from .models import CustomUser
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class SignUpTest(APITestCase):
    def test_signup_user(self):
        url = reverse('user-view')
        data = {'username': 'testuser', 'password': 'testpassword', 'password2': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())

    def test_signup_invalid_data(self):
        url = reverse('user-view')
        data = {'username': '', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
