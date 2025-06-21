from django.core.management.base import BaseCommand
from myapp.models import User

class Command(BaseCommand):
    help = 'Create sample users for testing'

    def handle(self, *args, **options):
        users = [
            # Managers
            {
                "email": "charles.freidenreich@shiftysolutions.com",
                "username": "charles",
                "first_name": "Charles",
                "last_name": "Freidenreich", 
                "password": "password123",
                "is_manager": True,
                "is_superuser": False,
                "is_staff": True,
            },
            {
                "email": "alex.smith@shiftysolutions.com",
                "username": "alexsmith",
                "first_name": "Alex",
                "last_name": "Smith",
                "password": "password123", 
                "is_manager": True,
                "is_superuser": False,
                "is_staff": True,
            },
            # Employees (non-managers)
            {
                "email": "alex.johnson@shiftysolutions.com",
                "username": "alexjohnson",
                "first_name": "Alex",
                "last_name": "Johnson",
                "password": "password123",
                "is_manager": False,
                "is_superuser": False,
                "is_staff": False,
            },
            {
                "email": "jamie.smith@shiftysolutions.com", 
                "username": "jamiesmith",
                "first_name": "Jamie",
                "last_name": "Smith",
                "password": "password123",
                "is_manager": False,
                "is_superuser": False,
                "is_staff": False,
            },
            {
                "email": "sarah.wilson@shiftysolutions.com",
                "username": "sarahwilson", 
                "first_name": "Sarah",
                "last_name": "Wilson",
                "password": "password123",
                "is_manager": False,
                "is_superuser": False,
                "is_staff": False,
            },
            {
                "email": "mike.chen@shiftysolutions.com",
                "username": "mikechen",
                "first_name": "Mike", 
                "last_name": "Chen",
                "password": "password123",
                "is_manager": False,
                "is_superuser": False,
                "is_staff": False,
            },
            {
                "email": "jane.doe@shiftysolutions.com",
                "username": "janedoe",
                "first_name": "Jane",
                "last_name": "Doe", 
                "password": "password123",
                "is_manager": False,
                "is_superuser": False,
                "is_staff": False,
            },
            {
                "email": "john.roe@shiftysolutions.com",
                "username": "johnroe",
                "first_name": "John",
                "last_name": "Roe",
                "password": "password123",
                "is_manager": False,
                "is_superuser": False,
                "is_staff": False,
            },
            {
                "email": "suyash.bhattarai@shiftysolutions.com",
                "username": "suyash",
                "first_name": "Suyash",
                "last_name": "Bhattarai",
                "password": "password123",
                "is_manager": False,
                "is_superuser": False,
                "is_staff": False,
            },
            # Admin user
            {
                "email": "admin@shiftysolutions.com",
                "username": "admin",
                "first_name": "System",
                "last_name": "Administrator",
                "password": "adminpass",
                "is_manager": False,
                "is_superuser": True,
                "is_staff": True,
            },
        ]

        created_count = 0
        for user_data in users:
            # Check both email and username to avoid conflicts
            if not User.objects.filter(email=user_data["email"]).exists() and not User.objects.filter(username=user_data["username"]).exists():
                try:
                    user = User.objects.create_user(
                        username=user_data["username"],
                        email=user_data["email"],
                        password=user_data["password"],
                        first_name=user_data.get("first_name", ""),
                        last_name=user_data.get("last_name", ""),
                    )
                    user.is_manager = user_data["is_manager"]
                    user.is_superuser = user_data["is_superuser"]
                    user.is_staff = user_data["is_staff"]
                    user.save()
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created user: {user.get_full_name()} ({user.email})')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creating user {user_data["email"]}: {str(e)}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User {user_data["email"]} already exists')
                )
        
        self.stdout.write(f'\n{self.style.SUCCESS(f"Created {created_count} new users")}')
        
        # List all users for verification
        self.stdout.write('\nAll users in database:')
        managers = User.objects.filter(is_manager=True)
        employees = User.objects.filter(is_manager=False, is_superuser=False)
        admins = User.objects.filter(is_superuser=True)
        
        if managers.exists():
            self.stdout.write(f'\n{self.style.SUCCESS("Managers:")}')
            for user in managers:
                self.stdout.write(f'- {user.get_full_name()} ({user.email})')
        
        if employees.exists():
            self.stdout.write(f'\n{self.style.SUCCESS("Employees:")}')
            for user in employees:
                self.stdout.write(f'- {user.get_full_name()} ({user.email})')
        
        if admins.exists():
            self.stdout.write(f'\n{self.style.SUCCESS("Administrators:")}')
            for user in admins:
                self.stdout.write(f'- {user.get_full_name()} ({user.email})')