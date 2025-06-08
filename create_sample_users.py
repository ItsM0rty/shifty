import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from myapp.models import User

def create_users():
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
        if not User.objects.filter(email=user_data["email"]).exists():
            user = User.objects.create_user(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"],
            )
            user.is_manager = user_data["is_manager"]
            user.is_superuser = user_data["is_superuser"]
            user.is_staff = user_data["is_staff"]
            user.save()
            print(f"Created user: {user.email}")
        else:
            print(f"User {user_data['email']} already exists.")

if __name__ == "__main__":
    create_users()
