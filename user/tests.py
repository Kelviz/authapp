from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Organization

User = get_user_model()

class UserRegistrationTest(APITestCase):
    def test_register_user_successfully_with_default_organisation(self):
        url = reverse('register')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'phone': '1234567890'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['data']['user']['first_name'], 'John')
        self.assertEqual(response.data['data']['user']['email'], 'john.doe@example.com')
        self.assertTrue(Organization.objects.filter(name="John's Organization").exists())




class UserRegistrationValidationTest(APITestCase):
    def test_missing_first_name(self):
        url = reverse('register')
        data = {
            'first_name': '',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'phone': '1234567890'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('first_name', response.data['error'], "Empty fields found: first_name")

    def test_missing_last_name(self):
        url = reverse('register')
        data = {
            'first_name': 'John',
            'last_name': '',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'phone': '1234567890'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('last_name', response.data['error'], "Empty fields found: last_name")

    def test_missing_email(self):
        url = reverse('register')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': '',
            'password': 'password123',
            'phone': '1234567890'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('email', response.data['error'], "Empty fields found: email")

    def test_missing_password(self):
        url = reverse('register')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'password': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data['error'], "Empty fields found: password")


class UserRegistrationDuplicateTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='john.doe@example.com',
            first_name='John',
            last_name='Doe',
            password='password123',
            phone='1234567890'
        )

    def test_duplicate_email(self):
        url = reverse('register')
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'phone': '0987654321'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['errors'], "user with this email already exists.")




class UserLoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='john.doe@example.com',
            first_name='John',
            last_name='Doe',
            password='password123',
            phone='1234567890'
        )

    def test_login_user_successfully(self):
        url = reverse('login')
        data = {
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['data']['user']['email'], 'john.doe@example.com')

    def test_login_user_unsuccessfully(self):
        url = reverse('login')
        data = {
            'email': 'john.doe@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Authentication failed')

