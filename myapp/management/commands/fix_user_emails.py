from django.core.management.base import BaseCommand
from myapp.models import User

class Command(BaseCommand):
    help = 'Fix email addresses for existing sample users'

    def handle(self, *args, **options):
        users_to_fix = [
            {'username': 'employee1', 'email': 'employee1@example.com'},
            {'username': 'manager1', 'email': 'manager1@example.com'},
            {'username': 'admin', 'email': 'admin@example.com'}
        ]
        
        for user_data in users_to_fix:
            try:
                user = User.objects.get(username=user_data['username'])
                if not user.email:
                    user.email = user_data['email']
                    user.save()
                    self.stdout.write(self.style.SUCCESS(
                        f'Updated email for {user.username}: {user.email}'
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'Email already set for {user.username}: {user.email}'
                    ))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f'User not found: {user_data["username"]}'
                ))
        
        # Verify fixes
        self.stdout.write('\nVerifying user emails:')
        for user in User.objects.all():
            self.stdout.write(f'- {user.username}: {user.email if user.email else "EMPTY"}')