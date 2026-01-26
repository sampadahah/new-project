from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    address= models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    

# Reference the custom user model used for auth
User = settings.AUTH_USER_MODEL


# Student profile table (admin manages this)
class Student(models.Model):
    # Optional link to login user account (can be used later)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Core student details
    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    program = models.CharField(max_length=100)
    batch = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"
    

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance")
    date = models.DateField(default=timezone.localdate)
    is_present = models.BooleanField(default=True)

    marked_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="marked_attendance"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "date")
        ordering = ["-date", "student__full_name"]

    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {'P' if self.is_present else 'A'}"