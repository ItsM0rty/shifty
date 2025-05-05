from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company, Shift, Availability, TimeOffRequest

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_manager')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'company_code', 'is_manager', 'hourly_rate', 'hire_date', 'profile_picture')}),
    )

class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_of_week', 'is_available', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'is_available')
    search_fields = ('user__username',)

class ShiftAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'start_time')
    search_fields = ('user__username', 'title')

class TimeOffRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'start_date')
    search_fields = ('user__username',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Company)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Availability, AvailabilityAdmin)
admin.site.register(TimeOffRequest, TimeOffRequestAdmin)
