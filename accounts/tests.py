from rest_framework.test import APIRequestFactory

# Using the standard RequestFactory API to create a form POST request

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status


class TestCase(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:verification')

    def test_post_phone_number_success(self):
        data = {"phone": "01012345678"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_post_phone_number_error(self):
        data = {"phone": "010123456abc"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)