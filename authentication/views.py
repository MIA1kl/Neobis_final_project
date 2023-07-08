from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegistrationSerializer, OTPVerificationSerializer, SignInSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

User = get_user_model()

class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            if User.objects.filter(phone_number=phone_number, registration_completed=False).exists():
                return Response({'detail': 'Verification code request already sent.'})
            verification_code = get_random_string(length=4, allowed_chars='0123456789')
            send_sms(phone_number, verification_code)
            user = User.objects.create(verification_code=verification_code, **serializer.validated_data)
            return Response({'detail': 'Please enter the OTP received via SMS. ' + verification_code})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OTPVerificationView(generics.GenericAPIView):
    serializer_class = OTPVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            entered_code = serializer.validated_data['verification_code']
            user = User.objects.filter(verification_code=entered_code).first()
            if user:
                user.is_active = True
                user.registration_completed=True
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
                verification_code = get_random_string(length=4, allowed_chars='0123456789')
                send_sms(phone_number, verification_code)
                user.verification_code = verification_code
                user.save()
                return Response({'detail': 'Please enter the OTP received via SMS. '+ verification_code})
            return Response({'detail': 'Invalid phone number or user not registered.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInOTPVerificationView(generics.GenericAPIView):
    serializer_class = OTPVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            entered_code = serializer.validated_data['verification_code']
            user = User.objects.filter(verification_code=entered_code).first()
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })
            return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def send_sms(phone_number, verification_code):
    # Use Twilio or any other SMS service provider to send the SMS
    # account_sid = 'your_account_sid'
    # auth_token = 'your_auth_token'
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(
    #     body=f'Your OTP for verification is: {otp}',
    #     from_='your_twilio_phone_number',
    #     to=phone_number
    # )
    print(f"The code is: {verification_code}")  # Replace this with actual SMS sending code
    
    

