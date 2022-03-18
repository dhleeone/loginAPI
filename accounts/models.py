from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(max_length=128, unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=45)
    phone = models.CharField(blank=True, max_length=20, unique=True)
