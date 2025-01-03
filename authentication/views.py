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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SignUpView(APIView):
    """
    ثبت نام کاربر جدید
    """
    @swagger_auto_schema(
        operation_description="Register a new user with email, phone number, and password.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email address. Must be unique.'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='User phone number in international format. Must be unique.'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for the user (optional).'),
            },
            required=['email', 'phone_number'],
        ),
        responses={
            201: openapi.Response(
                description="User registered successfully.",
                examples={
                    "application/json": {
                        "message": "User registered successfully. OTP sent.",
                        "user": {
                            "username": "example@example.com",
                            "email": "example@example.com",
                            "phone_number": "+123456789",
                        }
                    }
                }
            ),
            400: "Invalid input data.",
        },
    )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if not request.data.get('password'):
                otp = OTP.objects.create(user=user)
                otp.generate_otp()

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
    @swagger_auto_schema(
        operation_description="Send an OTP to the user based on their email or phone number.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'identifier': openapi.Schema(type=openapi.TYPE_STRING, description='User email or phone number.'),
            },
            required=['identifier'],
        ),
        responses={
            200: "OTP sent successfully!",
            404: "User not found.",
        },
    )
    def post(self, request):
        identifier = request.data.get('identifier') 
        try:
            user = User.objects.get(
                models.Q(email=identifier) | models.Q(phone_number=identifier)
            )
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

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
    @swagger_auto_schema(
        operation_description="Verify the OTP for a user using their email or phone number.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'identifier': openapi.Schema(type=openapi.TYPE_STRING, description='User email or phone number.'),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='The OTP value to verify.'),
            },
            required=['identifier', 'otp'],
        ),
        responses={
            200: "Access and refresh tokens returned.",
            401: "Invalid or expired OTP.",
            404: "User or OTP not found.",
        },
    )
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
            otp = user.otps.get(value=otp_value, is_active=True)
            if otp.is_valid():
                otp.is_active = False
                otp.save()

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
    @swagger_auto_schema(
        operation_description="Login a user with either password or OTP.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'identifier': openapi.Schema(type=openapi.TYPE_STRING, description='User email or phone number.'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password.'),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='User OTP.'),
            },
            required=['identifier'],
        ),
        responses={
            200: "Access and refresh tokens returned.",
            400: "Invalid input.",
            401: "Authentication failed.",
            404: "User not found.",
        },
    )
    def post(self, request):
        identifier = request.data.get('identifier')  
        password = request.data.get('password', None)
        otp_value = request.data.get('otp', None)
        if not identifier:
            return Response({"error": "Email or phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(
                models.Q(email=identifier) | models.Q(phone_number=identifier)
            )
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if password:
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)

        if otp_value:
            try:
                otp = user.otps.get(value=otp_value, is_active=True)
                if otp.is_valid():
                    otp.is_active = False
                    otp.save()

                    tokens = generate_tokens_for_user(user)
                    return Response(tokens, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "OTP is expired or invalid."}, status=status.HTTP_401_UNAUTHORIZED)
            except OTP.DoesNotExist:
                return Response({"error": "Invalid OTP for this user."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"error": "Provide either a password or OTP."}, status=status.HTTP_400_BAD_REQUEST)
