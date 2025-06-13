from django.core.management.base import BaseCommand
from myapp.models import User

class Command(BaseCommand):
    help = 'List all users in the database'

    def handle(self, *args, **options):
        users = User.objects.all()
        
        if users.exists():
            self.stdout.write(f'Found {users.count()} users in database:')
            self.stdout.write('-' * 50)
            
            for user in users:
                status_flags = []
                if user.is_superuser:
                    status_flags.append('superuser')
                if user.is_staff:
                    status_flags.append('staff')
                if hasattr(user, 'is_manager') and user.is_manager:
                    status_flags.append('manager')
                if user.is_active:
                    status_flags.append('active')
                else:
                    status_flags.append('inactive')
                
                status = ', '.join(status_flags) if status_flags else 'regular user'
                
                self.stdout.write(f'Email: {user.email}')
                self.stdout.write(f'Username: {user.username}')
                self.stdout.write(f'Status: {status}')
                self.stdout.write('-' * 30)
        else:
            self.stdout.write(self.style.WARNING('No users found in database'))