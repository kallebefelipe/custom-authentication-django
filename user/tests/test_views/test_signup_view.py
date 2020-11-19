import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User


class SignupViewTests(TestCase):

    def setUp(self):

        self.test_user = User.objects.create_user(
            'test@example.com', 'testpassword'
        )
        self.create_url = reverse('signup')
        self.client = APIClient()

    def test_create_user(self):
        data = {
            "first_name": "Hello",
            "last_name": "World",
            "email": "hello@world.com",
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
            self.create_url, data=json.dumps(data),
            content_type='application/json'
        )

        user = response.data['user']

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, 201)

        self.assertEqual(user['email'], data['email'])
        self.assertEqual(user['first_name'], data['first_name'])
        self.assertEqual(user['email'], data['email'])
        self.assertEqual(user['phones'], data['phones'])

        self.assertFalse('password' in response.data)

    def test_create_user_with_no_password(self):
        data = {
            "first_name": "Hello",
            "last_name": "World",
            "email": "hello@world.com",
            "phones": [
                {
                    "number": 988887888,
                    "area_code": 81,
                    "country_code": "+55"
                }
            ]
        }

        response = self.client.post(
            self.create_url, data, format='json'
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_invalid_email(self):
        data = {
            "first_name": "Hello",
            "last_name": "World",
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
            self.create_url, data, format='json'
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_preexisting_email(self):
        data = {
            "first_name": "Hello",
            "last_name": "World",
            "email": "test@example.com",
            "password": "hunter2",
            "phones": [
                {
                    "number": 988887888,
                    "area_code": 81,
                    "country_code": "+55"
                }
            ]
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_token(self):
        data = {
            "first_name": "Hello",
            "last_name": "World",
            "email": "hello@world.com",
            "password": "hunter2",
            "phones": [
                {
                    "number": 988887888,
                    "area_code": 81,
                    "country_code": "+55"
                }
            ]
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertTrue(response.data['token'])
