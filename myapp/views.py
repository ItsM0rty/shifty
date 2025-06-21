from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from myapp.models import User
from myapp.models import Shift
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import transaction
from myapp.models import TimeOffRequest

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


@login_required(login_url='/login')
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

        # Provide all required context variables dynamically
        now = timezone.now()
        start_of_week = now - timedelta(days=now.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=7)

        qs_week = Shift.objects.filter(user=request.user, start_time__gte=start_of_week, start_time__lt=end_of_week)

        # Hours this week
        hours_this_week = sum((s.end_time - s.start_time).total_seconds() for s in qs_week) / 3600 if qs_week.exists() else 0

        # Upcoming shifts (next 5)
        upcoming_qs = Shift.objects.filter(user=request.user, start_time__gte=now).order_by('start_time')[:5]
        upcoming_shifts = [
            {
                'title': s.title,
                'day': s.start_time.strftime('%A'),
                'time': f"{s.start_time.strftime('%I:%M %p').lstrip('0')} - {s.end_time.strftime('%I:%M %p').lstrip('0')}"
            }
            for s in upcoming_qs
        ]

        # Remaining shifts this week (scheduled but not started)
        remaining_shifts = qs_week.filter(start_time__gte=now).count()

        context = {
            'user': request.user,
            'remaining_shifts': remaining_shifts,
            'hours_this_week': round(hours_this_week, 1),
            'upcoming_shifts': upcoming_shifts,
            # Simple fields to avoid template errors
            'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            'time_slots': ['Morning', 'Afternoon', 'Evening'],
        }
        logger.debug("Context prepared successfully")
        response = render(request, 'myapp/dashboard.html', context)
        logger.debug("Dashboard template rendered successfully")
        return response
    except Exception as e:
        logger.error(f"Error in dashboard view: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
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
                    password=password,
                    is_active=False  # cannot log in until approved
                )
                
                # Set additional fields
                user.phone_number = phone_number
                user.company_code = company_code
                user.approved = False
                user.save()
                
                messages.info(request, "Account created. A manager must approve your signup before you can log in.")
                return redirect('myapp:login')
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

UserModel = get_user_model()


def _date_for_weekday(week_start: datetime.date, weekday_name: str):
    """Return the date object in the same week as week_start corresponding to weekday_name."""
    weekdays = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6,
    }
    index = weekdays.get(weekday_name.lower())
    if index is None:
        raise ValueError(f"Invalid weekday name: {weekday_name}")
    return week_start + timedelta(days=index)


@require_http_methods(["GET"])
@login_required(login_url='/login')
def api_employee_list(request):
    """Return a JSON list of all non-manager employees for the authenticated user's company."""
    if not request.user.is_staff:
        if not getattr(request.user, 'is_manager', False):
            return HttpResponseForbidden("Forbidden")

    employees = UserModel.objects.filter(is_manager=False).values('id', 'username', 'first_name', 'last_name', 'email')
    return JsonResponse({"employees": list(employees)}, status=200)


@require_http_methods(["GET"])
@login_required(login_url='/login')
def api_shift_list(request):
    """Return shifts in a given date range. Requires ?start=YYYY-MM-DD&end=YYYY-MM-DD or ?week_start=YYYY-MM-DD"""
    user = request.user
    start_date_str = request.GET.get('start')
    end_date_str = request.GET.get('end')
    week_start_str = request.GET.get('week_start')

    if week_start_str and not (start_date_str or end_date_str):
        # calculate full week range (Monday-Sunday) based on supplied week_start (Monday expected)
        try:
            week_start = datetime.strptime(week_start_str, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponseBadRequest("Invalid week_start format. Expected YYYY-MM-DD")
        start_date = week_start
        end_date = week_start + timedelta(days=6)
    elif start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponseBadRequest("Invalid start or end date format. Expected YYYY-MM-DD")
    else:
        return HttpResponseBadRequest("Provide week_start or start & end query parameters")

    qs = Shift.objects.filter(start_time__date__gte=start_date, end_time__date__lte=end_date)
    if not (user.is_staff or getattr(user, 'is_manager', False)):
        qs = qs.filter(user=user)

    shifts_data = []
    for shift in qs.select_related('user'):
        shifts_data.append({
            'id': shift.id,
            'user_id': shift.user.id,
            'user_name': shift.user.get_full_name() or shift.user.username,
            'start_time': shift.start_time.isoformat(),
            'end_time': shift.end_time.isoformat(),
            'manual_override': shift.manual_override,
            'status': shift.status,
            'title': shift.title,
        })

    return JsonResponse({'shifts': shifts_data}, status=200)


@csrf_exempt  # Front-end will include CSRF token later, but allow for now.
@require_http_methods(["POST"])
@login_required(login_url='/login')
@transaction.atomic
def api_shift_bulk_save(request):
    """Bulk create or update shifts. Only staff can call."""
    if not request.user.is_staff:
        if not getattr(request.user, 'is_manager', False):
            return HttpResponseForbidden("Forbidden")

    import json
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON body")

    week_start_str = payload.get('week_start')
    shifts = payload.get('shifts', [])
    if not week_start_str or not shifts:
        return HttpResponseBadRequest("Missing week_start or shifts list")

    try:
        week_start = datetime.strptime(week_start_str, "%Y-%m-%d").date()
    except ValueError:
        return HttpResponseBadRequest("Invalid week_start format; expected YYYY-MM-DD")

    created_ids = []
    updated_ids = []

    for entry in shifts:
        try:
            user_id = entry['employee_id']
            day = entry['day']  # e.g., "Monday"
            start_time_str = entry['start']  # "09:00"
            end_time_str = entry['end']  # "17:00"
            manual_override = bool(entry.get('manual_override', False))
            title = entry.get('title', 'Shift')
        except KeyError:
            return HttpResponseBadRequest("Shift entry missing required keys")

        try:
            user_obj = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return HttpResponseBadRequest(f"User {user_id} not found")

        shift_date = _date_for_weekday(week_start, day)
        try:
            start_t = datetime.strptime(start_time_str, "%H:%M").time()
            end_t = datetime.strptime(end_time_str, "%H:%M").time()
        except ValueError:
            return HttpResponseBadRequest("Invalid time format. Expected HH:MM")

        start_dt = timezone.make_aware(datetime.combine(shift_date, start_t))
        end_dt = timezone.make_aware(datetime.combine(shift_date, end_t))

        # Upsert: if a shift already exists for user with overlapping times on that date, update it.
        existing = Shift.objects.filter(user=user_obj, start_time__date=shift_date, title=title).first()
        if existing:
            existing.start_time = start_dt
            existing.end_time = end_dt
            existing.manual_override = manual_override
            existing.status = 'scheduled'
            existing.save()
            updated_ids.append(existing.id)
        else:
            new_shift = Shift.objects.create(
                user=user_obj,
                start_time=start_dt,
                end_time=end_dt,
                title=title,
                description='',
                status='scheduled',
                manual_override=manual_override
            )
            created_ids.append(new_shift.id)

    return JsonResponse({'created': created_ids, 'updated': updated_ids}, status=201)

@login_required(login_url='/login')
@csrf_exempt
def api_timeoff(request):
    """Employees: GET their requests, POST to create. Managers: GET pending requests."""
    if request.method == 'GET':
        if request.user.is_staff or getattr(request.user, 'is_manager', False):
            # Managers see pending requests across employees
            qs = TimeOffRequest.objects.filter(status='pending').select_related('user')
        else:
            qs = TimeOffRequest.objects.filter(user=request.user).select_related('user')
        data = [
            {
                'id': t.id,
                'user_id': t.user.id,
                'user_name': t.user.get_full_name() or t.user.username,
                'start_date': t.start_date.isoformat(),
                'end_date': t.end_date.isoformat(),
                'reason': t.reason,
                'status': t.status,
            }
            for t in qs.order_by('-created_at')
        ]
        return JsonResponse({'requests': data}, status=200)

    # POST - create new request (employee only)
    import json
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    start_date = payload.get('start_date')
    end_date = payload.get('end_date')
    reason = payload.get('reason', '')
    if not (start_date and end_date):
        return HttpResponseBadRequest("start_date and end_date are required")
    try:
        sd = datetime.strptime(start_date, "%Y-%m-%d").date()
        ed = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return HttpResponseBadRequest("Dates must be YYYY-MM-DD")
    if ed < sd:
        return HttpResponseBadRequest("end_date must be after start_date")

    req = TimeOffRequest.objects.create(user=request.user, start_date=sd, end_date=ed, reason=reason)
    return JsonResponse({'id': req.id, 'status': req.status}, status=201)


@csrf_exempt
@require_http_methods(["POST"])
@login_required(login_url='/login')
def api_timeoff_decision(request, pk):
    """Managers approve/deny a time-off request."""
    try:
        req = TimeOffRequest.objects.get(pk=pk)
    except TimeOffRequest.DoesNotExist:
        return HttpResponseBadRequest("Request not found")

    if not (request.user.is_staff or getattr(request.user, 'is_manager', False)):
        return HttpResponseForbidden("Forbidden")

    import json
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    decision = payload.get('decision')  # 'approved' or 'denied'
    if decision not in ['approved', 'denied']:
        return HttpResponseBadRequest("Invalid decision value")

    req.status = decision
    req.save()
    return JsonResponse({'id': req.id, 'status': req.status}, status=200)

# -------------------- Sign-up approval API --------------------

@require_http_methods(["GET"])
@login_required(login_url='/login')
def api_pending_signups(request):
    """List users awaiting approval (approved=False)"""
    if not (request.user.is_staff or getattr(request.user, 'is_manager', False)):
        return HttpResponseForbidden("Forbidden")

    pending_qs = UserModel.objects.filter(approved=False).values('id', 'username', 'first_name', 'last_name', 'email', 'date_joined')
    return JsonResponse({'pending': list(pending_qs)}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
@login_required(login_url='/login')
def api_signup_decision(request, pk):
    """Approve or reject a pending signup."""
    if not (request.user.is_staff or getattr(request.user, 'is_manager', False)):
        return HttpResponseForbidden("Forbidden")

    try:
        user_obj = UserModel.objects.get(pk=pk, approved=False)
    except UserModel.DoesNotExist:
        return HttpResponseBadRequest("User not found or already decided")

    import json
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    decision = payload.get('decision')
    if decision not in ['approve', 'reject']:
        return HttpResponseBadRequest("Invalid decision value")

    if decision == 'approve':
        user_obj.approved = True
        user_obj.is_active = True
        user_obj.save()
    else:
        # Reject: delete the user
        user_obj.delete()
    return JsonResponse({'id': pk, 'status': decision}, status=200)
