# your_app/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Here, 'username' is actually the phone number.
            user = UserModel.objects.get(phone_number=username)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
