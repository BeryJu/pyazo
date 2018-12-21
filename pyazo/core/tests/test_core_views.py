"""test core views"""
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase

from pyazo.core.models import Collection
from pyazo.core.tests.utils import test_auth


class CoreViewTests(TestCase):
    """Test core views"""

    def test_index(self):
        """Test default index page"""
        self.client.login(**test_auth())
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_not_super(self):
        """Test default index page as a normal user"""
        self.client.login(**test_auth(superuser=False))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_paginator(self):
        """Test invalid paginator page"""
        self.client.login(**test_auth())
        response = self.client.get(reverse('index')+'?page=3')
        self.assertEqual(response.status_code, 200)

    def test_index_collection(self):
        """Test valid collection"""
        self.client.login(**test_auth())
        Collection.objects.create(name='test', owner=User.objects.first())
        response = self.client.get(reverse('index')+'?collection=test')
        self.assertEqual(response.status_code, 200)

    def test_index_collection_invalid(self):
        """Test invalid collection"""
        self.client.login(**test_auth())
        response = self.client.get(reverse('index')+'?collection=aa')
        self.assertEqual(response.status_code, 404)
