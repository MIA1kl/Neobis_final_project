from rest_framework import serializers
from .models import User

class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth', 'phone_number']

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        user = super().create(validated_data)
        user.phone_number = phone_number
        user.save()
        return user

class OTPVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=4, max_length=4)

class SignInSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
