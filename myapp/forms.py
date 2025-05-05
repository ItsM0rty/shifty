from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class SignUpForm(UserCreationForm):
    """
    Form for user registration with custom fields.
    
    This form extends Django's UserCreationForm to include additional fields
    like email, phone number, and company code.
    """
    email = forms.EmailField(
        max_length=254, 
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'hello@shiftysolutions.com'})
    )
    phone_number = forms.CharField(
        max_length=15, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '(555) 123-4567'})
    )
    company_code = forms.CharField(
        max_length=50, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your company code'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'company_code', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make username field optional if you want to use email as the primary identifier
        # self.fields['username'].required = False
        
        # Add placeholders and classes to the default fields
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'placeholder': '••••••••'})
        self.fields['password2'].widget.attrs.update({'placeholder': '••••••••'})


class LoginForm(forms.Form):
    """
    Form for user login.
    """
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )
    remember_me = forms.BooleanField(required=False)

    # CLOUD MIGRATION NOTE:
    # Form validation works the same regardless of database backend
    # No changes needed when migrating to cloud
