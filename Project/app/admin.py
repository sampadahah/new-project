from django.contrib import admin

from .models import Attendance, CustomUser, Student 
# Register your models here.

admin.site.register(Attendance)
admin.site.register(CustomUser)
admin.site.register(Student)


