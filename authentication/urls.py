from django.urls import path
from .views import SignUpView, LoginView, SendOTPView, VerifyOTPView

urlpatterns = urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign_up'),       # مسیر ثبت‌نام
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),    # مسیر ارسال OTP
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),  # مسیر تأیید OTP
    path('login/', LoginView.as_view(), name='login'),            # مسیر ورود
]
