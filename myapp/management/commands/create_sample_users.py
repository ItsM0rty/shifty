from django.core.management.base import BaseCommand
from myapp.models import User

class Command(BaseCommand):
    help = 'Create sample users for testing'

    def handle(self, *args, **options):
        users = [
            {
                "email": "employee1@example.com",
                "username": "employee1",
                "password": "password123",
                "is_manager": False,
                "is_superuser": False,
                "is_staff": False,
            },
            {
                "email": "manager1@example.com",
                "username": "manager1",
                "password": "password123",
                "is_manager": True,
                "is_superuser": False,
                "is_staff": False,
            },
            {
                "email": "admin@example.com",
                "username": "admin",
                "password": "adminpass",
                "is_manager": False,
                "is_superuser": True,
                "is_staff": True,
            },
        ]

        for user_data in users:
            # Check both email and username to avoid conflicts
            if not User.objects.filter(email=user_data["email"]).exists() and not User.objects.filter(username=user_data["username"]).exists():
                try:
                    user = User.objects.create_user(
                        username=user_data["username"],
                        email=user_data["email"],
                        password=user_data["password"],
                    )
                    user.is_manager = user_data["is_manager"]
                    user.is_superuser = user_data["is_superuser"]
                    user.is_staff = user_data["is_staff"]
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created user: {user.email}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creating user {user_data["email"]}: {str(e)}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User {user_data["email"]} already exists')
                )
        
        # List all users for verification
        self.stdout.write('\nAll users in database:')
        for user in User.objects.all():
            self.stdout.write(f'- {user.email} (username: {user.username})')