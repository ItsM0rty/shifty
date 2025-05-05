from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    """
    Home page view.
    """
    return render(request, 'myapp/home.html')

def about_view(request):
    """
    About page view.
    """
    return render(request, 'myapp/about.html')

def contact_view(request):
    """
    Contact page view.
    """
    return render(request, 'myapp/contact.html')

def sales_view(request):
    """
    Sales page view.
    """
    return render(request, 'myapp/sales.html')

def user_login(request):
    """
    Handle user login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if not remember_me:
                # Session expires when browser closes
                request.session.set_expiry(0)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('myapp:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'myapp/login.html')

@login_required
def dashboard(request):
    """
    User dashboard view.
    """
    return render(request, 'myapp/dashboard.html')

def signup_view(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        # Basic form handling for now
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        phone_number = request.POST.get('phone_number', '')
        company_code = request.POST.get('company_code', '')
        password = request.POST.get('password', '')
        
        # Simple validation
        if not (email and password):
            messages.error(request, "Please fill in all required fields.")
        else:
            # Create user
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                
                # If username is not provided, use email as username
                if not username:
                    username = email
                    
                user = User.objects.create_user(
                    username=username, 
                    email=email, 
                    password=password
                )
                
                # Set additional fields
                user.phone_number = phone_number
                user.company_code = company_code
                user.save()
                
                # Log the user in
                login(request, user)
                messages.success(request, "Account created successfully!")
                return redirect('myapp:dashboard')
            except Exception as e:
                messages.error(request, f"Error creating account: {str(e)}")
    
    return render(request, 'myapp/signup.html')

def user_logout(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('myapp:login')
