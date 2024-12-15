from django.urls import path
from .views import TokenObtainPairView, TokenRefreshView,SendOTPView, VerifyOTPView,CombinedLoginView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('otp/send/', SendOTPView.as_view(), name='send_otp'),
    path('otp/verify/', VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', CombinedLoginView.as_view(), name='combined_login'),
]