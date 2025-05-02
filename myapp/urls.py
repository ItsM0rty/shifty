from django.urls import path, include
from . import views 

app_name = 'myapp' 

urlpatterns = [
    path('', views.home, name='home'),

    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('sales/', views.sales_view, name='sales'),
    path('login/', views.login_view, name='login'),

]
