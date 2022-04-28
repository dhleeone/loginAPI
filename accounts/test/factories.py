import factory
from faker import Faker
from django.contrib.auth.hashers import make_password
from ..views import PhoneVerify
from ..models import *
import random


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = Faker().name()
    nickname = Faker().name()
    email = factory.lazy_attribute(lambda u: f"{u.name.split()[0]}@example.com")
    phone = "010123456" + str(random.randint(0, 9))
    password = make_password("qwer1234")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = "test"
    nickname = "test1"
    email = factory.lazy_attribute(lambda u: f"{u.name}@google.com")
    phone = "01012345678"
    password = make_password("qwer1234")


