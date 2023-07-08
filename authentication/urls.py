from django.urls import path
from .views import (
    RegistrationView, OTPVerificationView, SignInView, SignInOTPVerificationView
)

urlpatterns = [
    path('register/phone', RegistrationView.as_view(), name='register'),
    path('register/verify', OTPVerificationView.as_view(), name='otp-verify'),
    path('login/phone', SignInView.as_view(), name='sign-in'),
    path('login/verify', SignInOTPVerificationView.as_view(), name='sign-in-otp-verify'),
]
