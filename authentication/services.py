from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

def generate_tokens_for_user(user):
    """
    این تابع توکن‌های دسترسی و رفرش را برای کاربر تولید می‌کند
    """
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

def send_otp_email(user, otp):
    """
    ارسال OTP به ایمیل - در محیط توسعه فقط لاگ می‌کند
    """
    print(f"[TEST MODE] Sending OTP to {user.email}: {otp}")


def send_otp_sms(phone_number, otp):
    """
    ارسال OTP به شماره تلفن - در محیط توسعه فقط لاگ می‌کند
    """
    print(f"[TEST MODE] Sending OTP to {phone_number}: {otp}")