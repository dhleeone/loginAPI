from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import timedelta
from django.utils.timezone import now


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('The given email mist be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username='', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, password, username='', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self._create_user(email, username, password, **extra_fields)


# 유저 ---
class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(max_length=128, unique=True)
    username = models.CharField(max_length=30, blank=True)
    nickname = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=45)
    phone = models.CharField(max_length=20, unique=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# 전화번호 인증 ---
class PhoneVerification(models.Model):
    phone = models.CharField(max_length=20)
    security_code = models.CharField(max_length=20, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} - {str(self.timestamp)[:10]}"

    @property
    def is_expired(self):
        expire_time = self.timestamp + timedelta(minutes=5)
        if now() > expire_time:
            return True
        return False

