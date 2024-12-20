from rest_framework import serializers
from .models import User, OTP, UserDetail, Role, UserRole, UserMoreInfo, UserMoreInfoKey, UserMoreInfoKeyRole
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},  # پسورد الزامی نیست
        }

    def validate_email(self, value):
        """
        بررسی یکتا بودن ایمیل
        """
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_phone_number(self, value):
        """
        بررسی یکتا بودن شماره تلفن
        """
        if value and User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value
    
    def create(self, validated_data):
        """
        ایجاد کاربر با تنظیم خودکار username براساس ایمیل یا شماره تلفن
        """
        # استخراج ایمیل و شماره تلفن از داده‌های ارسال شده
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')

        # تنظیم username براساس ایمیل یا شماره تلفن
        if email:
            validated_data['username'] = email
        elif phone_number:
            validated_data['username'] = phone_number
        else:
            raise serializers.ValidationError("Either email or phone number must be provided.")

        # جدا کردن پسورد
        password = validated_data.pop('password', None)

        # ایجاد کاربر
        user = User.objects.create(**validated_data)

        # تنظیم پسورد اگر وارد شده باشد
        if password:
            user.set_password(password)
            user.save()

        return user
    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['user', 'firstname', 'lastname', 'address', 'location']

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['user', 'value', 'is_active', 'created_at']

    def generate_otp(self, user):
        otp, created = OTP.objects.get_or_create(user=user)
        otp.generate_otp()
        return otp

class SignInSerializer(serializers.Serializer):
    identifier = serializers.CharField()  
    password = serializers.CharField(required=False)
    otp = serializers.CharField(required=False)

class OTPRequestSerializer(serializers.Serializer):
    identifier = serializers.CharField()

class TokenObtainSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['user', 'role']

class UserMoreInfoKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMoreInfoKey
        fields = ['name']

class UserMoreInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMoreInfo
        fields = ['user', 'key', 'value', 'role']

class UserMoreInfoKeyRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMoreInfoKeyRole
        fields = ['key', 'role']