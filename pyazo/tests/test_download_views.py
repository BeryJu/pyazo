"""test download views"""
import os

from django.conf import settings
from django.shortcuts import reverse
from django.test import TestCase

from pyazo.tests.utils import test_auth


class DownloadViewTests(TestCase):
    """Test all client download views"""

    def setUp(self):
        super().setUp()
        os.makedirs(os.path.join(settings.BASE_DIR+"/", 'bin/'), exist_ok=True)

    def test_windows(self):
        """Test windows download"""
        exe_path = os.path.join(settings.BASE_DIR+"/", 'bin/', 'Pyazo.exe')
        with open(exe_path, 'w') as _file:
            _file.write('test')
        self.client.login(**test_auth())
        response = self.client.get(reverse('download_client_windows'))
        self.assertEqual(response['Content-Type'], 'application/octet-stream')
        self.assertEqual(response.status_code, 200)

    def test_windows_404(self):
        """Test windows download but with missing file"""
        exe_path = os.path.join(settings.BASE_DIR+"/", 'bin/', 'Pyazo.exe')
        os.unlink(exe_path)
        self.client.login(**test_auth())
        response = self.client.get(reverse('download_client_windows'))
        self.assertEqual(response.status_code, 404)

    def test_sharex(self):
        """Test shareX"""
        self.client.login(**test_auth())
        response = self.client.get(reverse('download-sxcu'))
        self.assertEqual(response.status_code, 200)

    def test_macos(self):
        """Test macos download"""
        exe_path = os.path.join(settings.BASE_DIR+"/", 'bin/', 'pyazo.dmg')
        with open(exe_path, 'w') as _file:
            _file.write('test')
        self.client.login(**test_auth())
        response = self.client.get(reverse('download_client_macos'))
        self.assertEqual(response['Content-Type'], 'application/x-apple-diskimage')
        self.assertEqual(response.status_code, 200)

    def test_macos_404(self):
        """Test macos download but with missing file"""
        exe_path = os.path.join(settings.BASE_DIR+"/", 'bin/', 'pyazo.dmg')
        os.unlink(exe_path)
        self.client.login(**test_auth())
        response = self.client.get(reverse('download_client_macos'))
        self.assertEqual(response.status_code, 404)
