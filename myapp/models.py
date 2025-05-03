from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

class User(AbstractUser):
    # Basic user information
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    company_code = models.CharField(max_length=50, blank=True, null=True)
    
    # Additional fields
    is_manager = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # Fix for the reverse accessor clash
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="custom_user_groups",  # Changed from default
        related_query_name="custom_user",
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="custom_user_permissions",  # Changed from default
        related_query_name="custom_user",
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    
    def __str__(self):
        return self.username


# Company Model
# -------------
# For storing company information
class Company(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True, null=True)
    
    # CLOUD MIGRATION NOTE:
    # For multi-tenant applications in the cloud, you might add:
    # subscription_tier = models.CharField(max_length=20, choices=[...])
    # max_employees = models.IntegerField(default=10)
    
    def __str__(self):
        return self.name
