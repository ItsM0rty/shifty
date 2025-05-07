from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging
from django.http import HttpResponse
from myapp.models import User

def home(request):
    """
    Home page view.
    """
    return render(request, 'myapp/index.html')

def about_view(request):
    """
    About page view.
    """
    return render(request, 'myapp/about.html')

def test_db(request):
    users = User.objects.all()
    return HttpResponse(f"Found {users.count()} users in the database.")

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

logger = logging.getLogger(__name__)

def login_view(request):
    # Add debug logging to see what's happening
    logger.debug("Login view accessed")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        logger.debug(f"Login attempt with username: {username}")
        
        # Print the credentials (only in development!)
        print(f"Login attempt - Username: {username}, Password: {password}")
        
        # Try to authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Authentication successful
            logger.debug(f"Authentication successful for {username}")
            login(request, user)
            logger.debug("User logged in, redirecting to dashboard")
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('myapp:dashboard')  # Make sure this URL name exists
        else:
            # Authentication failed
            logger.debug(f"Authentication failed for {username}")
            messages.error(request, "Invalid username or password. Please try again.")
            return render(request, 'myapp/login.html', {'username': username})
    
    # GET request - just show the login form
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
