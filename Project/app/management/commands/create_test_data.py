from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app.models import Student, Attendance
from django.utils import timezone
from datetime import datetime, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test data for student attendance system'

    def handle(self, *args, **options):
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_superuser': True,
                'is_staff': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user: admin/admin123'))

        # Create test student user
        student_user, created = User.objects.get_or_create(
            username='john_doe',
            defaults={
                'email': 'john.doe@example.com',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        if created:
            student_user.set_password('student123')
            student_user.save()
            self.stdout.write(self.style.SUCCESS('Created student user: john_doe/student123'))

        # Create student record
        student, created = Student.objects.get_or_create(
            student_id='STU001',
            defaults={
                'user': student_user,
                'full_name': 'John Doe',
                'email': 'john.doe@example.com',
                'program': 'Computer Science',
                'batch': '2024'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created student record: STU001'))

        # Create attendance records for the last 30 days
        today = timezone.localdate()
        for i in range(30):
            date = today - timedelta(days=i)
            # Skip weekends for more realistic data
            if date.weekday() < 5:  # Monday = 0, Sunday = 6
                attendance, created = Attendance.objects.get_or_create(
                    student=student,
                    date=date,
                    defaults={
                        'is_present': random.choice([True, True, True, False]),  # 75% attendance
                        'marked_by': admin_user
                    }
                )
                if created:
                    status = "Present" if attendance.is_present else "Absent"
                    self.stdout.write(f'Created attendance for {date}: {status}')

        self.stdout.write(self.style.SUCCESS('Test data creation completed!'))
        self.stdout.write('You can now login with:')
        self.stdout.write('Admin: admin/admin123')
        self.stdout.write('Student: john_doe/student123')