"""test utils"""

from django.shortcuts import reverse
from django.test import TestCase
from django.test.client import RequestFactory

from pyazo.root.celery import after_task_publish, config_loggers
from pyazo.utils import get_client_ip, get_reverse_dns


class UtilsTest(TestCase):
    """Test utils"""

    def setUp(self):
        self.factory = RequestFactory()

    def test_remote_ip(self):
        """test get_client_ip"""
        with self.assertRaises(ValueError):
            get_client_ip(None)
        request = self.factory.get(reverse("index"))
        request.META["REMOTE_ADDR"] = "aa"
        self.assertEqual(get_client_ip(request), "aa")

    def test_reverse_dns(self):
        """Test get_reverse_dns"""
        self.assertEqual(get_reverse_dns("erqwer"), "")

    def test_celery(self):
        """Test celery setup"""
        config_loggers()
        after_task_publish(headers={}, body={})
