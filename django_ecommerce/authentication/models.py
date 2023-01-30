from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from datetime import datetime, timedelta

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10,blank = True)
    otp = models.CharField(max_length=6,blank = True)
    otp_expiry = models.DateTimeField(default=datetime.now() - timedelta(minutes=5))
    is_verified = models.BooleanField(default=False)

