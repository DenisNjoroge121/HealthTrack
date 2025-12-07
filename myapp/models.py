from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role='patient', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, role='doctor', **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )
    full_name = models.CharField(max_length=30)
    email=models.EmailField(max_length=30)
    specialization = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)  # Changed from IntegerField

    def __str__(self):
        return f"Dr. {self.user.full_name} ({self.specialization})"
    
    @property
    def email(self):
        return self.user.email
    
    @property
    def name(self):
        return self.user.full_name

class Patient(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='patient_account',
        null=True,
        blank=True
    )
    # doctor = models.ForeignKey(
    #     Doctor, 
    #     on_delete=models.SET_NULL, 
    #     null=True, 
    #     blank=True,
    #     related_name='patients'
    # )
    full_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    symptoms = models.TextField(blank=False, null=False)
    diagnosis = models.TextField(blank=False, null=False)
    prescription = models.TextField(blank=False, null=False)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.full_name
    
    # @property
    # def full_name(self):
    #     return self.user.full_name if self.user else "Unknown"
    
    # @property
    # def email(self):
    #     return self.user.email if self.user else ""

class Record(models.Model):
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='records')
    profile_picture = models.ImageField(upload_to='patient_pics/', null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    exercise_type = models.CharField(max_length=50)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    age = models.DecimalField(max_digits=3,decimal_places=0)

    def __str__(self):
        return self.date

class Message(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message_text = models.TextField()
    # doctor = models.ForeignKey(
    #     Doctor,
    #     on_delete=models.CASCADE,
    #     related_name='messages_received'
    # )
    # sender = models.ForeignKey(
    #     CustomUser,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='sent_messages'
    # )
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.full_name} to Dr. {self.doctor.user.full_name}"
    

