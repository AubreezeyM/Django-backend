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

    def test_get_all_users(self):
        url = reverse('get_all_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)


class ProfileAPITests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    # --- GET TESTS ---
    def test_get_profile_authenticated(self):
        """Authenticated users can retrieve their profile"""
        url = reverse('profile_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bio', response.data)  # Check for profile fields

    def test_get_profile_unauthenticated(self):
        """Unauthenticated requests are rejected"""
        self.client.credentials()  # Remove auth token
        url = reverse('profile_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- PUT TESTS ---
    def test_update_profile(self):
        """Users can update their own profile"""
        url = reverse('profile_detail')
        update_data = {
            'bio': 'New bio text',
            'location': 'Berlin'
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'New bio text')
        self.assertEqual(self.user.profile.location, 'Berlin')

    def test_partial_update(self):
        """PATCH updates should work (partial fields)"""
        url = reverse('profile_detail')
        response = self.client.patch(url, {'bio': 'Partial update'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.profile.bio, 'Partial update')

    # --- SECURITY TESTS ---
    def test_cannot_modify_other_user_profile(self):
        """Users can't modify another user's profile"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass'
        )
        other_profile = other_user.profile
        
        url = reverse('profile_detail')
        response = self.client.put(url, {'bio': 'Hacked!'})
        
        # Original profile unchanged
        other_profile.refresh_from_db()
        self.assertNotEqual(other_profile.bio, 'Hacked!')