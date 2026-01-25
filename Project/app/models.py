from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

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