import factory
from django.contrib.auth.hashers import make_password
from ..views import PhoneVerify
from ..models import *


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = "test@google.com"
    nickname = "test"
    phone = "01012345678"
    password = make_password("qwer1234")

