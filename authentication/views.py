from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from django.contrib.auth import authenticate
from .models import User, OTP,UserDetail
from rest_framework_simplejwt.tokens import RefreshToken
from .services import send_otp_email, send_otp_sms
from .serializers import (
    OTPRequestSerializer,
    OTPSerializer,
    TokenObtainSerializer,
    TokenRefreshSerializer,
    SignInSerializer,
    UserSerializer,
    UserDetailSerializer,
    UserRoleSerializer,
    UserMoreInfoSerializer
)
from .tokens import generate_tokens_for_user

class SignUpView(APIView):
    """
    ثبت نام کاربر جدید
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # بررسی اینکه پسورد ارسال نشده است
            if not request.data.get('password'):
                # تولید OTP برای کاربر
                otp = OTP.objects.create(user=user)
                otp.generate_otp()

                # ارسال OTP به شماره تلفن
                send_otp_sms(user.phone_number, otp.value)

                return Response({
                    "message": "User registered successfully. OTP sent.",
                    "user": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                "message": "User registered successfully. You can log in with your password.",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SendOTPView(APIView):
    """
    ارسال OTP به کاربر
    """
    def post(self, request):
        identifier = request.data.get('identifier')  # شماره تلفن یا ایمیل
        try:
            user = User.objects.get(
                models.Q(email=identifier) | models.Q(phone_number=identifier)
            )
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # تولید و ارسال OTP
        otp_value = user.otps.create().value
        if user.phone_number == identifier:
            send_otp_sms(user.phone_number, otp_value)
        elif user.email == identifier:
            send_otp_email(user.email, otp_value)

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

        # بررسی OTP
        try:
            otp = user.otps.get(value=otp_value, is_active=True)
            if otp.is_valid():
                otp.is_active = False
                otp.save()

                # تولید توکن
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_401_UNAUTHORIZED)

        except OTP.DoesNotExist:
            return Response({"error": "OTP not found."}, status=status.HTTP_404_NOT_FOUND)
        

class LoginView(APIView):
    """
    ورود کاربر با OTP یا پسورد
    """
    def post(self, request):
        identifier = request.data.get('identifier')  # شماره تلفن یا ایمیل
        password = request.data.get('password', None)
        otp_value = request.data.get('otp', None)
        if not identifier:
            return Response({"error": "Email or phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # یافتن کاربر بر اساس ایمیل یا شماره تلفن
            user = User.objects.get(
                models.Q(email=identifier) | models.Q(phone_number=identifier)
            )
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # ورود با پسورد
        if password:
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)

        # ورود با OTP
        if otp_value:
            try:
                # بررسی اینکه OTP برای کاربر فعلی است
                otp = user.otps.get(value=otp_value, is_active=True)
                if otp.is_valid():
                    otp.is_active = False
                    otp.save()

                    # تولید توکن
                    tokens = generate_tokens_for_user(user)
                    return Response(tokens, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "OTP is expired or invalid."}, status=status.HTTP_401_UNAUTHORIZED)
            except OTP.DoesNotExist:
                return Response({"error": "Invalid OTP for this user."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"error": "Provide either a password or OTP."}, status=status.HTTP_400_BAD_REQUEST)
