from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    # Basic user information
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    company_code = models.CharField(max_length=50, blank=True, null=True)
    
    # Additional fields
    is_manager = models.BooleanField(default=False)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    hire_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    # Indicates if the user has been approved by a manager/admin
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class Company(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

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
    
    # Indicates if this shift was manually overridden by a manager
    manual_override = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}: {self.title} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"

class Availability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability')
    
    # Day choices
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    is_available = models.BooleanField(default=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'day_of_week')
        verbose_name_plural = 'Availabilities'
    
    def __str__(self):
        status = "Available" if self.is_available else "Unavailable"
        if self.is_available and self.start_time and self.end_time:
            return f"{self.user.username}: {self.get_day_of_week_display()} - {status} from {self.start_time} to {self.end_time}"
        return f"{self.user.username}: {self.get_day_of_week_display()} - {status}"

class TimeOffRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='time_off_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True, null=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}: {self.start_date} to {self.end_date} ({self.status})"
