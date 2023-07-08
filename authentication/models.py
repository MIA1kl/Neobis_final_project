from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

class User(AbstractUser):
    username = None 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    verification_code = models.CharField(max_length=4, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    
    USERNAME_FIELD='phone_number'

    def __str__(self):
        return self.phone_number

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }