from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from user.models import Phone, User


class MeViewTests(TestCase):

    def setUp(self):
        self.enc_password = make_password('hunter2')
        self.user = baker.make(
            User, email='tester@world.com', password=self.enc_password,
            first_name='Hello', last_name='World',
        )
        baker.make(
            Phone, number=988887888, area_code=81, country_code="+55",
            user=self.user
        )
        self.url = reverse('me')
        self.client = APIClient()

    def test_user_token(self):
        data = {
            "first_name": "Hello",
            "last_name": "World",
            "email": "tester@world.com",
            "password": "hunter2",
            "phones": [
                {
                    "number": 988887888,
                    "area_code": 81,
                    "country_code": "+55"
                }
            ]
        }
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)
        user = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(user['email'], data['email'])
        self.assertEqual(user['first_name'], data['first_name'])
        self.assertEqual(user['email'], data['email'])
        self.assertEqual(user['phones'], data['phones'])

    def test_user_invalid(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
