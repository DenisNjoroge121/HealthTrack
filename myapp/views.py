from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import CustomUser, Doctor, Patient, Record, Message
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.role == role:
                login(request, user)
                if role == 'doctor':
                    return redirect('doctor')
                else:
                    return redirect('patient')
            else:
                messages.error(request, f"Please login as {user.role.title()}")
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, 'login.html')

def register_user(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'register.html')

        try:
            with transaction.atomic():
                # Create the user
                user = CustomUser.objects.create_user(
                    email=email,
                    password=password1,
                    role=role,
                    full_name=full_name
                )
                
                # Create profile based on role
                if role == 'doctor':
                    if not hasattr(user, 'doctor_profile'):
                        Doctor.objects.create(user=user)
                    else:
                        messages.warning(request, "Doctor profile already exists for this user.")
                elif role == 'patient':
                    if not hasattr(user, 'patient_account'):
                        Patient.objects.create(user=user)
                    else:
                        messages.warning(request, "Patient profile already exists for this user.")
                
                messages.success(request, "Account created successfully! Please login.")
                return redirect('login')
                
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
    
    return render(request, 'register.html')

@login_required
def doctor(request):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied. Only doctors can view this page.")
        return redirect('home')
    patients= Patient.objects.all()
    return render(request, 'doctor.html',{'patients': patients})

@login_required
def add_patient(request):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied.")
        return redirect('home')
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        symptoms = request.POST.get('symptoms')
        diagnosis = request.POST.get('diagnosis')
        prescription = request.POST.get('prescription')
        date = request.POST.get('date')

        Patient.objects.create(
            full_name=full_name,
            age=age,
            email=email,
            gender=gender,
            symptoms=symptoms,
            diagnosis=diagnosis,
            prescription=prescription,
            date=date
        )
        messages.success(request, "Patient added successfully!")
        return redirect('doctor')
    return render(request, 'add_patient.html')

@login_required
def patient(request):
    if request.user.role != 'patient':
        messages.error(request, "Access denied. Only patients can view this page.")
        return redirect('home')
    records = Record.objects.all()
    return render(request, 'patient.html',{'records':records})

@login_required
def add_record(request):
    if request.user.role != 'patient':
        messages.error(request, "Access denied.")
        return redirect('home')
    if request.method =='POST':
        exercise_type = request.POST.get('exercise_type')
        hours = request.POST.get('hours')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        profile_picture = request.FILES.get('profile_picture')
        age = request.POST.get('age')

        Record.objects.create(
            exercise_type=exercise_type,
            hours=hours,
            weight=weight,
            height=height,
            profile_picture=profile_picture,
            age=age
        )
        messages.success(request, "Record added successfully!")
        return redirect('patient')
    return render(request, 'add_record.html')

@login_required
def add_doctor(request):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied.")
        return redirect('home')
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        specialization = request.POST.get('specialization')
        department = request.POST.get('department')
        phone_number = request.POST.get('phone_number')

        Doctor.objects.create.all(
            full_name=full_name,
            email=email,
            specialization=specialization,
            department=department,
            phone_number=phone_number
        )
        messages.success(request, "Doctor added successfully!")
        return redirect('doctor')
    return render(request, 'add_doctor.html')

@login_required
def messagedoctor(request):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied.")
        return redirect('home')
    all_messages = Message.objects.all()
    return render(request, 'messagedoctor.html', {'all_messages': all_messages})

@login_required
def add_message(request):
    if request.user.role != 'patient':
        messages.error(request, "Access denied.")
        return redirect('home')
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message_text = request.POST.get('message_text')

        Message.objects.create(
                    full_name=full_name,
                    email=email,
                    phone_number=phone_number,
                    message_text=message_text,
                )
        messages.success(request, "Message sent successfully!")
        return redirect('patient')
    return render(request, 'add_message.html')

@login_required
def edit_patient(request, patient_id):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied.")
        return redirect('home')
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        patient.age = request.POST.get('age')
        patient.gender = request.POST.get('gender')
        patient.symptoms = request.POST.get('symptoms')
        patient.diagnosis = request.POST.get('diagnosis')
        patient.prescription = request.POST.get('prescription')
        patient.save()
        messages.success(request, "Patient updated successfully!")
        return redirect('doctor')
    return render(request, 'edit_patient.html', {"patient": patient})

def about(request):
    return render(request, 'about.html')

def education(request):
    return render(request, 'education.html')

def aboutdo(request):
    return render(request, 'aboutdo.html')

def patdoctor(request):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied.")
        return redirect('home')
    doctors = Doctor.objects.all()
    return render(request, 'patdoctor.html',{'doctors':doctors})