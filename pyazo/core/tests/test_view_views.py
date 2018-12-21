"""test view views"""
import os

from django.conf import settings
from django.shortcuts import reverse
from django.test import TestCase

from pyazo.core.models import Upload


class UploadViewTests(TestCase):
    """Test upload views"""

    def setUp(self):
        super().setUp()
        self.test_file_path = settings.MEDIA_ROOT + 'test.txt'
        with open(self.test_file_path, 'w') as _file:
            self._test_data = 'testdatafewrqwer'
            _file.write(self._test_data)
        self.upload = Upload.objects.create(file=self.test_file_path)

    def tearDown(self):
        super().tearDown()
        os.unlink(self.test_file_path)

    def _view_helper(self, view_name, file_hash):
        """test upload view"""
        response = self.client.get(reverse(view_name, kwargs={'file_hash': file_hash}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), self._test_data)

    def test_view_sha512_short(self):
        """Test sha512_short"""
        self._view_helper('view_sha512_short', self.upload.sha512_short)

    def test_view_md5(self):
        """Test view_md5"""
        self._view_helper('view_md5', self.upload.md5)

    def test_view_sha256(self):
        """Test view_sha256"""
        self._view_helper('view_sha256', self.upload.sha256)

    def test_view_sha512(self):
        """Test view_sha512"""
        self._view_helper('view_sha512', self.upload.sha512)

    def test_404(self):
        """Test not found upload"""
        response = self.client.get(
            reverse('view_sha512_short', kwargs={'file_hash': 'abcdefghijklmnop'}))
        self.assertEqual(response.status_code, 404)

    def test_thumbnail(self):
        """Test thumbnail upload"""
        response = self.client.get(
            reverse('view_sha512_short', kwargs={'file_hash': self.upload.sha512_short}) + '?thumb')
        self.assertEqual(response.status_code, 200)
