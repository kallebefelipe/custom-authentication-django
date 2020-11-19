import json

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from user.models import Phone, User


class SigninViewTests(TestCase):

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
        self.url = reverse('signin')
        self.client = APIClient()

    def test_valid_signin(self):
        data = {
            "email": "tester@world.com",
            "password": "hunter2"
        }

        user_info = {
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

        response = self.client.post(
            self.url, data=json.dumps(data),
            content_type='application/json'
        )

        user = response.data['user']

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(user['email'], user_info['email'])
        self.assertEqual(user['first_name'], user_info['first_name'])
        self.assertEqual(user['email'], user_info['email'])
        self.assertEqual(user['phones'], user_info['phones'])

        self.assertFalse('password' in response.data)

    def test_create_user_invalid_email(self):
        data = {
            "email": "hunter@world.com",
            "password": "hunter2"
        }

        response = self.client.post(
            self.url, data, format='json'
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
