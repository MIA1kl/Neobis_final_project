from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    otp = models.CharField(max_length=4, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    
    USERNAME_FIELD='phone_number'

    def __str__(self):
        return self.phone_number
