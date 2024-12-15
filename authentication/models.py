from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
import random

class UserManager(BaseUserManager):
    def create_user(self, username=None, email=None, phone_number=None, password=None, **extra_fields):
        if not username and not email and not phone_number:
            raise ValueError(_('The username, email, or phone number must be set.'))

        if email:
            email = self.normalize_email(email)

        user = self.model(username=username, email=email, phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150, unique=True, null=True, blank=True,
        help_text=_('A unique username for the user.')
    )
    email = models.EmailField(
        unique=True, null=True, blank=True, validators=[EmailValidator()],
        help_text=_('User email address.')
    )
    phone_number = models.CharField(
        max_length=15, unique=True, null=True, blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        help_text=_('User phone number in international format.')
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'  
    REQUIRED_FIELDS = ['email', 'phone_number'] 

    def __str__(self):
        return self.username or self.email or self.phone_number

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='details')
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
    
class UserMoreInfoKey(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class UserMoreInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='more_info')
    key = models.ForeignKey(UserMoreInfoKey, on_delete=models.CASCADE, related_name='info')
    value = models.TextField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='more_info', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.key.name}"
    
class UserMoreInfoKeyRole(models.Model):
    key = models.ForeignKey(UserMoreInfoKey, on_delete=models.CASCADE, related_name='key_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_keys')

    def __str__(self):
        return f"{self.key.name} - {self.role.name}"
    
class SecurityEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='security_events')
    ip = models.GenericIPAddressField()
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    logout_reason = models.TextField(null=True, blank=True)
    agent = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"SecurityEvent: {self.user.username}"
    
class OTP(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='otps')
    value = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def generate_otp(self):
        """
        تولید کد OTP
        """
        self.value = f"{random.randint(100000, 999999)}"
        self.is_active = True
        self.save()

    def is_valid(self):
        """
        اعتبارسنجی مدت اعتبار OTP (۵ دقیقه)
        """
        return self.is_active and (now() - self.created_at).seconds < 300

    def __str__(self):
        return f"OTP for {self.user}: {self.value}"