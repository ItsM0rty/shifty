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
    logger.debug("Login view accessed")
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        logger.debug(f"Login attempt with email: {email}")
        
        try:
            # Authenticate using custom email backend by passing both username and email
            logger.debug(f"Attempting authentication for email: {email}")
            user = authenticate(request, username=email, email=email, password=password)
            
            if user is not None:
                # Authentication successful
                logger.debug(f"Authentication successful for {email}")
                login(request, user)
                logger.debug("User logged in, redirecting to dashboard")
                messages.success(request, f"Welcome back, {user.email}!")
                return redirect('myapp:dashboard')
            else:
                # Authentication failed
                logger.debug(f"Authentication failed for {email}")
                
                # Additional debugging: Check if user exists but password is wrong
                try:
                    user = User.objects.get(email__iexact=email)
                    logger.debug(f"User exists but password is invalid: {user}")
                except User.DoesNotExist:
                    logger.debug(f"No user found with email: {email}")
                except Exception as e:
                    logger.debug(f"Error checking user existence: {str(e)}")
                
                messages.error(request, "Invalid email or password. Please try again.")
                return render(request, 'myapp/login.html', {'email': email})
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            messages.error(request, "An unexpected error occurred during authentication. Please try again.")
            return render(request, 'myapp/login.html', {'email': email})
    
    # GET request - just show the login form
    return render(request, 'myapp/login.html')


@login_required(login_url='/login')  # Fixed: Added login_url parameter
def dashboard(request):
    """
    User dashboard view.
    """
    logger.debug("Dashboard view accessed")
    
    try:
        # Log user information
        logger.debug(f"User authenticated: {request.user.is_authenticated}")
        logger.debug(f"User ID: {request.user.id}")
        logger.debug(f"User email: {request.user.email}")
        
        # Test database connection
        logger.debug("Testing database connection...")
        try:
            user_count = User.objects.count()
            logger.debug(f"Total users in database: {user_count}")
        except Exception as db_err:
            logger.error(f"Database connection failed: {str(db_err)}")
            logger.error(f"DB error type: {type(db_err).__name__}")
            messages.error(request, "Database connection issue. Please try again later.")
            return render(request, 'myapp/error.html', {'error': 'Database connection failed'}, status=500)
        
        # Test user object access
        logger.debug("Testing user object access...")
        user_data = {
            'id': request.user.id,
            'email': request.user.email,
            'first_name': getattr(request.user, 'first_name', 'N/A'),
            'last_name': getattr(request.user, 'last_name', 'N/A'),
            'is_staff': request.user.is_staff,
        }
        logger.debug(f"User data: {user_data}")
        
        # Test template context
        context = {
            'user': request.user
        }
        logger.debug("Context prepared successfully")
        
        # Attempt to render template
        logger.debug("Attempting to render dashboard template...")
        response = render(request, 'myapp/dashboard.html', context)
        logger.debug("Dashboard template rendered successfully")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in dashboard view: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        
        # Return user-friendly error page
        return render(request, 'myapp/error.html', {'error': str(e)}, status=500)


from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def admin_dashboard(request):
    """
    Admin dashboard view.
    Only accessible by staff members or superusers.
    """
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access the admin dashboard")
        return redirect('myapp:dashboard')
    return render(request, 'myapp/admin_dashboard.html')

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

def test_static(request):
    """
    Test view for verifying static file serving
    """
    try:
        return render(request, 'myapp/test_static.html')
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error rendering test_static.html: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return HttpResponse("Error rendering template", status=500)

def static_test(request):
    """
    Simple view to test static file serving
    """
    context = {'works': True}
    return render(request, 'myapp/static_test.html', context)
