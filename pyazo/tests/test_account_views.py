"""test pyazo's account views"""
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase


class AccountViewTests(TestCase):
    """Test views in views/accounts.py"""

    def setUp(self):
        super().setUp()
        self.invalid_data = {}
        self.invalid_creds = {
            'username': 'test',
            'password': 'test23',
            'remember': False
        }
        self.valid_data = {
            'username': 'test',
            'password': 'test',
            'remember': False
        }
        User.objects.create_user(username='test', password='test')
        self.url = reverse('accounts-login')

    def test_login_get(self):
        """Test login view"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_post_valid(self):
        """Test valid login"""
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

    def test_login_post_next(self):
        """Test valid login + next param"""
        response = self.client.post(self.url+'?next=/test', self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/test')

    def test_login_post_invalid_form(self):
        """Test invalid login (inalid form data)"""
        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.status_code, 200)

    def test_login_post_invalid_creds(self):
        """Test invalid login (inalid creds data)"""
        response = self.client.post(self.url, self.invalid_creds)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url)

    def test_logout(self):
        """Test logout view"""
        self.client.login(**self.valid_data)
        response = self.client.get(reverse('accounts-logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))
