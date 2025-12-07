"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('login/', views.user_login, name='login'),
    path('register/', views.register_user, name='register'),
    # path('logout/', views.logout_view, name='logout'),
    
    # Doctor routes
    path('doctor/', views.doctor, name='doctor'),
    path('doctor/add-patient/', views.add_patient, name='add_patient'),
    path('doctor/add-doctor/', views.add_doctor, name='add_doctor'),
    path('doctor/messages/', views.messagedoctor, name='messagedoctor'),
    # path('doctor/patient/<int:pk>/', views.view_patient_profile, name='patient_profile'),
    path('doctor/patient/<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    # path('doctor/delete/<int:id>/', views.delete_patient, name='delete'),
    
    # Patient routes
    path('patient/', views.patient, name='patient'),
    path('patient/add-record/', views.add_record, name='add_record'),
    path('patient/doctors/', views.patdoctor, name='patdoctor'),
    path('patient/message/', views.add_message, name='add_message'),
    
    # General routes
    path('about/', views.about, name='about'),
    path('education/', views.education, name='education'),
    path('aboutdo/', views.aboutdo, name='aboutdo'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)