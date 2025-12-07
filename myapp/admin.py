from django.contrib import admin

from myapp.models import Message, Patient, Record, Doctor

# Register your models here.

admin.site.register(Patient)
admin.site.register(Record)
admin.site.register(Doctor)
admin.site.register(Message)
