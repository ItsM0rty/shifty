from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# User Model
# ----------
# This extends Django's built-in user model with additional fields
# This approach works well for both local and cloud databases

class User(AbstractUser):
    # Basic user information
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    company_code = models.CharField(max_length=50, blank=True, null=True)
    
    # Additional fields you might need
    is_manager = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # CLOUD MIGRATION NOTE:
    # This model structure will work the same in cloud databases
    # No changes needed to the model when migrating

    def __str__(self):
        return self.username

# Shift Model
# -----------
# For storing shift information
class Shift(models.Model):
    # Relationship to user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shifts')
    
    # Shift details
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    # Status options
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
        ('swapped', 'Swapped'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # CLOUD MIGRATION NOTE:
    # Time fields work the same in cloud databases
    # For high-volume applications, you might want to add database indexes
    # class Meta:
    #     indexes = [models.Index(fields=['start_time', 'user'])]

    def __str__(self):
        return f"{self.user.username}: {self.title} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"

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
