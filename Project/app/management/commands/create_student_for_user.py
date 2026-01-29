from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app.models import Student

User = get_user_model()

class Command(BaseCommand):
    help = 'Create student record for existing user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to create student record for')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            
            # Check if student record already exists
            if hasattr(user, 'student'):
                self.stdout.write(self.style.WARNING(f'Student record already exists for {username}'))
                return
            
            # Create student record
            student = Student.objects.create(
                user=user,
                student_id=f'STU{user.id:03d}',
                full_name=f'{user.first_name} {user.last_name}' if user.first_name else user.username,
                email=user.email or f'{user.username}@example.com',
                program='Computer Science',
                batch='2024'
            )
            
            self.stdout.write(self.style.SUCCESS(f'Successfully created student record for {username}'))
            self.stdout.write(f'Student ID: {student.student_id}')
            self.stdout.write(f'Full Name: {student.full_name}')
            self.stdout.write(f'Email: {student.email}')
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist'))