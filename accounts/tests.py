from .views import PhoneVerify
from django.shortcuts import redirect, resolve_url
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status
from accounts.models import *


class PhoneVerificationTestCase(APITestCase):
    def setUp(self):
        self.url = resolve_url('/accounts/verification')

    def test_post_phone_number_success(self):
        data = {"phone": "01012345678"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_post_phone_number_error(self):
        data = {"phone": "010123456abc"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RegisterTestCase(APITestCase):
    def setUp(self):
        self.url = resolve_url('/accounts/register')
        self.phone_verify = PhoneVerification.objects.create(phone="01012345678", security_code=PhoneVerify.generate_code(self))

    def test_register_success(self):
        data = {
            "email": "test6@google.com",
            "password": "qwer1234",
            "password2": "qwer1234",
            "nickname": "test6",
            "name": "테스트",
            "phone": self.phone_verify.phone,
            "security_code": self.phone_verify.security_code
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_passoword_too_short_error(self):
        data = {
            "email": "test6@google.com",
            "password": "qr12",
            "password2": "qw12",
            "nickname": "test6",
            "name": "테스트",
            "phone": self.phone_verify.phone,
            "security_code": self.phone_verify.security_code
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_passoword_email_same_error(self):
        data = {
            "email": "test6@google.com",
            "password": "test6",
            "password2": "test6",
            "nickname": "test",
            "name": "테스트",
            "phone": self.phone_verify.phone,
            "security_code": self.phone_verify.security_code
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(APITestCase):
    def setUp(self):
        self.url = resolve_url('/accounts/login')
        self.user = User.objects.create(
            email="test@google.com",
            nickname="test",
            phone="01012345678"
        )
        self.user.set_password("qwer1234")
        self.user.save()

    def test_login_success(self):
        data = {
            "email": "test@google.com",
            "password": "qwer1234",
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class ProfileTestCase(APITestCase):
    def setUp(self):
        self.url = resolve_url('/accounts/profile')
        self.user = User.objects.create(
            email="test@google.com",
            nickname="test",
            name="test",
            phone="01012345678",
        )
        self.user.set_password("qwer1234")
        self.user.save()

    def test_get_profile(self):
        self.client.login(email="test@google.com", password="qwer1234")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
