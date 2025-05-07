from django.urls import path, include
from . import views 

app_name = 'myapp' 

urlpatterns = [
    path('', views.home, name='home'),
    path('test-db/', views.test_db, name='test_db'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('sales/', views.sales_view, name='sales'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.user_logout, name='logout'),

]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]