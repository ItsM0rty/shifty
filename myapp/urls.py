# myapp/urls.py
from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('test-db/', views.test_db, name='test_db'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('sales/', views.sales_view, name='sales'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('test-static/', views.test_static, name='test_static'),
    path('static-test/', views.static_test, name='static_test'),
    path('api/employees/', views.api_employee_list, name='api_employee_list'),
    path('api/shifts/', views.api_shift_list, name='api_shift_list'),
    path('api/shifts/bulk-save/', views.api_shift_bulk_save, name='api_shift_bulk_save'),
    path('api/timeoff/', views.api_timeoff, name='api_timeoff'),
    path('api/timeoff/<int:pk>/decision/', views.api_timeoff_decision, name='api_timeoff_decision'),
]
