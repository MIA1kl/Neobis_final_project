from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegistrationSerializer, OTPVerificationSerializer, SignInSerializer
User = get_user_model()

class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = get_random_string(length=4, allowed_chars='0123456789')
            send_sms(phone_number, otp)
            user = User.objects.create(otp=otp, **serializer.validated_data)
            return Response({'detail': 'Please enter the OTP received via SMS. '+otp})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OTPVerificationView(generics.GenericAPIView):
    serializer_class = OTPVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            entered_code = serializer.validated_data['code']
            user = User.objects.filter(otp=entered_code).first()
            if user:
                user.is_active = True
                user.save()
                return Response({'detail': 'Registration successful.'})
            return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInView(generics.GenericAPIView):
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = User.objects.filter(phone_number=phone_number).first()
            if user and user.is_active:
                otp = get_random_string(length=4, allowed_chars='0123456789')
                send_sms(phone_number, otp)
                user.otp = otp
                user.save()
                return Response({'detail': 'Please enter the OTP received via SMS.'})
            return Response({'detail': 'Invalid phone number or user not registered.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInOTPVerificationView(generics.GenericAPIView):
    serializer_class = OTPVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            entered_code = serializer.validated_data['code']
            user = User.objects.filter(otp=entered_code).first()
            if user:
                return Response({'detail': 'Sign-in successful.'})
            return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_sms(phone_number, otp):
    # Use Twilio or any other SMS service provider to send the SMS
    # account_sid = 'your_account_sid'
    # auth_token = 'your_auth_token'
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(
    #     body=f'Your OTP for verification is: {otp}',
    #     from_='your_twilio_phone_number',
    #     to=phone_number
    # )
    print(f"The code is: {otp}")  # Replace this with actual SMS sending code
