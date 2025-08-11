import uuid

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserAPITests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'aubrey',
            'password': 'password',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)

    def test_login_success(self):
        url = reverse('login')
        data = self.user_data
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_failure(self):
        url = reverse('login')
        data = {
            'username': 'wronguser',
            'password': 'wrongpass'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user(self):
        unique_id = uuid.uuid4().hex[:8]
        url = reverse('create_user')
        username = f'testuser_{unique_id}'
        data = {
            'username': username,
            'password': 'newpass123',
            'email': f'new_{unique_id}@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

        user_exists = User.objects.filter(username=username).exists()
        self.assertTrue(user_exists, 'User should exist in database.')

    def test_validate_token(self):
        url = reverse('validate_token')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {'message': f'Test for {self.user.username} passed!'}
        )