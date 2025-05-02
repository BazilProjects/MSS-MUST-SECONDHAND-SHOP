from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
#from cloudinary.models import CloudinaryField
from django.conf import settings
from django.urls import reverse


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    is_new = models.BooleanField(default=False)
    is_old = models.BooleanField(default=False)
    image1 = models.ImageField(upload_to='media/products/', default=None)

    '''
    image1 = CloudinaryField('image', folder='products/', blank=True, null=True)
    image2 = CloudinaryField('image', folder='products/', blank=True, null=True)
    image3 = CloudinaryField('image', folder='products/', blank=True, null=True)
    image4 = CloudinaryField('image', folder='products/', blank=True, null=True)
    '''
    def __str__(self):
        return f"{self.name} by {self.user.phone_number}"

    def get_absolute_url(self):
        # build URL using the product’s numeric ID
        return reverse("product_detail", kwargs={"pk": self.pk})


"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, pin=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number field is required")

        if pin and (not pin.isdigit() or len(pin) > 4):  # Ensure pin is numeric and max 4 digits
            raise ValueError("PIN must be a numeric string with a maximum of 4 digits.")

        user = self.model(phone_number=phone_number, **extra_fields)
        if pin:
            user.set_password(pin)  # Use PIN as a password
        else:
            user.set_unusable_password()  # Handle case where PIN is not set
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, pin=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone_number, pin, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    pin = models.CharField(max_length=4)  # Restrict PIN to 4 digits
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_set', blank=True)

    def __str__(self):
        return self.phone_number
"""
# your_app/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, pin, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number must be set")
        if not pin:
            raise ValueError("A PIN is required")
        user = self.model(phone_number=phone_number, **extra_fields)
        # Set the user’s password to the PIN (this hashes it)
        user.set_password(pin)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, pin, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, pin, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    pin = models.CharField(max_length=4)  # Stored for reference; authentication uses the hashed password.
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []  # No additional required fields

    # Required for admin permissions:
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
    )

    def __str__(self):
        return self.phone_number
