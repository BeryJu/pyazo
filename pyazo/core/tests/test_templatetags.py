"""test template tags commands"""
from django.shortcuts import reverse
from django.test import RequestFactory, TestCase

from pyazo.core.templatetags.pyazo import back


class TemplateTagTest(TestCase):
    """Test django template tags"""

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def test_back(self):
        """Test back"""
        initial_request = self.factory.get(reverse('index'))
        self.assertEqual(back({'request': initial_request}), '')
        get_back_request = self.factory.get(reverse('index') + '?back=external')
        self.assertEqual(back({'request': get_back_request}), 'external')
        meta_request = self.factory.get(reverse('index'))
        meta_request.META['HTTP_REFERER'] = 'external'
        self.assertEqual(back({'request': meta_request}), 'external')
