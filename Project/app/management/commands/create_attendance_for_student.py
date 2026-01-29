from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app.models import Student, Attendance
from django.utils import timezone
from datetime import datetime, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create attendance records for a student'

    def add_arguments(self, parser):
        parser.add_argument('student_id', type=str, help='Student ID to create attendance for')

    def handle(self, *args, **options):
        student_id = options['student_id']
        
        try:
            student = Student.objects.get(student_id=student_id)
            admin_user = User.objects.filter(is_superuser=True).first()
            
            # Create attendance records for the last 30 days
            today = timezone.localdate()
            created_count = 0
            
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
                        created_count += 1
                        status = "Present" if attendance.is_present else "Absent"
                        self.stdout.write(f'Created attendance for {date}: {status}')
            
            self.stdout.write(self.style.SUCCESS(f'Created {created_count} attendance records for {student.full_name}'))
            
        except Student.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Student with ID {student_id} does not exist'))