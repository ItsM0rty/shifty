import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from myapp.models import User

def create_users():
    users = [
        {
            "username": "employee1",
            "password": "password123",
            "is_manager": False,
            "is_superuser": False,
            "is_staff": False,
        },
        {
            "username": "manager1",
            "password": "password123",
            "is_manager": True,
            "is_superuser": False,
            "is_staff": False,
        },
        {
            "username": "admin",
            "password": "adminpass",
            "is_manager": False,
            "is_superuser": True,
            "is_staff": True,
        },
    ]

    for user_data in users:
        if not User.objects.filter(username=user_data["username"]).exists():
            user = User.objects.create_user(
                username=user_data["username"],
                password=user_data["password"],
            )
            user.is_manager = user_data["is_manager"]
            user.is_superuser = user_data["is_superuser"]
            user.is_staff = user_data["is_staff"]
            user.save()
            print(f"Created user: {user.username}")
        else:
            print(f"User {user_data['username']} already exists.")

if __name__ == "__main__":
    create_users()
