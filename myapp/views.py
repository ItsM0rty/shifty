from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('myapp:dashboard')  # Using namespace
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'myapp/login.html')

def user_logout(request):
    logout(request)
    return redirect('myapp:login')

@login_required(login_url='myapp:login')  # Updated with namespace
def dashboard(request):
    return render(request, 'myapp/dashboard.html')


def home(request):
    return render(request, 'myapp/index.html')

def about_view(request):
    return render(request, 'myapp/about.html', {})

def contact_view(request):
    return render(request, 'myapp/contact.html', {})

def sales_view(request):
    return render(request, 'myapp/sales.html', {})

# def login_view(request):
#     return render(request, 'myapp/login.html', {})

# Add this new function to handle signups
def signup_view(request):
    return render(request, 'myapp/signup.html', {})
