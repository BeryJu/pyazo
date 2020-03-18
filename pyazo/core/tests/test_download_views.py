"""test download views"""
import os

from django.conf import settings
from django.shortcuts import reverse
from django.test import TestCase

from pyazo.core.tests.utils import test_auth


class DownloadViewTests(TestCase):
    """Test all client download views"""

    def setUp(self):
        super().setUp()
        os.makedirs(os.path.join(settings.BASE_DIR + "/", "bin/"), exist_ok=True)

    def test_windows(self):
        """Test windows download"""
        self.client.login(**test_auth())
        response = self.client.get(
            reverse("download-client", kwargs={"client": "windows"})
        )
        self.assertEqual(response["Content-Type"], "application/octet-stream")
        self.assertEqual(response.status_code, 200)

    def test_sharex(self):
        """Test shareX"""
        self.client.login(**test_auth())
        response = self.client.get(
            reverse("download-client", kwargs={"client": "sharex"})
        )
        self.assertEqual(response.status_code, 200)

    def test_macos(self):
        """Test macos download"""
        self.client.login(**test_auth())
        response = self.client.get(
            reverse("download-client", kwargs={"client": "macos"})
        )
        self.assertEqual(response["Content-Type"], "application/x-apple-diskimage")
        self.assertEqual(response.status_code, 200)
