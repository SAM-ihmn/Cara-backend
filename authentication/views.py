from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from .tokens import generate_tokens_for_user
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, OTP
from .services import send_otp_email, send_otp_sms

class SendOTPView(APIView):
    """
    ارسال OTP به کاربر
    """
    def post(self, request):
        identifier = request.data.get('identifier')  # ایمیل یا شماره تلفن

        try:
            user = User.objects.get(
                models.Q(email=identifier) | models.Q(phone_number=identifier)
            )
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # ایجاد یا به‌روزرسانی OTP
        otp, created = OTP.objects.get_or_create(user=user)
        otp.generate_otp()

        # ارسال OTP
        if user.email == identifier:
            send_otp_email(user, otp.value)
        elif user.phone_number == identifier:
            send_otp_sms(user.phone_number, otp.value)

        return Response({"message": "OTP sent successfully!"}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    """
    تأیید OTP
    """
    def post(self, request):
        identifier = request.data.get('identifier')
        otp_value = request.data.get('otp')

        try:
            user = User.objects.get(
                models.Q(email=identifier) | models.Q(phone_number=identifier)
            )
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            otp = OTP.objects.get(user=user, value=otp_value, is_active=True)
            if otp.is_valid():
                otp.is_active = False
                otp.save()
                return Response({"message": "OTP verified successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "OTP is expired or invalid."}, status=status.HTTP_401_UNAUTHORIZED)
        except OTP.DoesNotExist:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_401_UNAUTHORIZED)
        
class TokenObtainPairView(APIView):
    """
    صدور توکن دسترسی و رفرش
    """
    def post(self, request):
        identifier = request.data.get('identifier')  # یوزرنیم، ایمیل یا شماره تلفن
        password = request.data.get('password')

        try:
            user = User.objects.get(
                models.Q(username=identifier) |
                models.Q(email=identifier) |
                models.Q(phone_number=identifier)
            )
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # احراز هویت
        user = authenticate(username=user.username, password=password)
        if not user:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # صدور توکن
        tokens = generate_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)


class TokenRefreshView(APIView):
    """
    نوسازی توکن دسترسی با استفاده از توکن رفرش
    """
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({"access": access_token}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED)
        
class CombinedLoginView(APIView):
    """
    ورود ترکیبی با OTP یا رمز عبور
    """
    def post(self, request):
        identifier = request.data.get('identifier')  # ایمیل، شماره تلفن یا یوزرنیم
        password = request.data.get('password', None)
        otp_value = request.data.get('otp', None)

        try:
            user = User.objects.get(
                models.Q(username=identifier) |
                models.Q(email=identifier) |
                models.Q(phone_number=identifier)
            )
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # ورود با رمز عبور
        if password:
            user = authenticate(username=user.username, password=password)
            if user:
                tokens = generate_tokens_for_user(user)
                return Response(tokens, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # ورود با OTP
        if otp_value:
            try:
                otp = OTP.objects.get(user=user, value=otp_value, is_active=True)
                if otp.is_valid():
                    otp.is_active = False
                    otp.save()
                    tokens = generate_tokens_for_user(user)
                    return Response(tokens, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "OTP is expired or invalid."}, status=status.HTTP_401_UNAUTHORIZED)
            except OTP.DoesNotExist:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"error": "Provide either a password or OTP."}, status=status.HTTP_400_BAD_REQUEST)