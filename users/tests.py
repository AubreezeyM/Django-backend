from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile

User = get_user_model()

class AuthTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.profile = Profile.objects.get(user=self.user)

    def test_user_registration(self):
        url = reverse('create_user')
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'new@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertIn('access', response.data)

    def test_login_success(self):
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_invalid_credentials(self):
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'wrongpass'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint(self):
        url = reverse('profile_detail')
        
        # Unauthenticated request
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Authenticated request
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'new user')

    def test_profile_update(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        profile = Profile.objects.get(user=self.user)
        
        url = reverse('profile_detail')
        data = {'bio': 'Updated bio'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile.refresh_from_db()
        self.assertEqual(profile.bio, 'Updated bio')

    def test_profile_auto_creation_signal(self):
        new_user = User.objects.create_user(
            username='signaluser',
            password='testpass'
        )
        self.assertTrue(hasattr(new_user, 'profile'), 
            "Profile should be automatically created via signals")