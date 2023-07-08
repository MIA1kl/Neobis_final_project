from django.urls import path
from .views import (
    RegistrationView, OTPVerificationView, SignInView, SignInOTPVerificationView
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('otp-verify/', OTPVerificationView.as_view(), name='otp-verify'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('sign-in-otp-verify/', SignInOTPVerificationView.as_view(), name='sign-in-otp-verify'),
]
