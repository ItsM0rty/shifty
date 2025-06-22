from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    """
    Custom authentication backend that authenticates users using their email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user based on email address and password.
        """
        UserModel = get_user_model()

        # Retrieve the email from kwargs or fall back to the username parameter.
        email = kwargs.get("email") or username
        if email is None or password is None:
            return None

        try:
            user = UserModel.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            return None

        # Respect inactive or unapproved flags
        if not (user.is_active and getattr(user, 'approved', True)):
            return None

        try:
            if user.check_password(password):
                return user
        except Exception:
            # In case of unusable password etc.
            return None

        return None

    def get_user(self, user_id):
        """
        Retrieve a User instance by ID.
        """
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None