"""test management commands"""
import os

from django.conf import settings
from django.test import TestCase

from pyazo.core.management.commands.re_index import Command as ReIndexCommand
from pyazo.core.models import Object


class ManagementTests(TestCase):
    """Test django management commands"""

    def test_re_index(self):
        """Test re_index command"""
        with open(settings.MEDIA_ROOT + "test.txt", "w") as _file:
            _file.write("test")
        with open(settings.MEDIA_ROOT + "test2.txt", "w") as _file:
            _file.write("updating existing upload")
        Object.objects.create(file=settings.MEDIA_ROOT + "test2.txt")
        count_before = len(Object.objects.all())
        self.assertEqual(ReIndexCommand().handle(), 0)
        # We expect reindex to create one new upload
        self.assertEqual(len(Object.objects.all()), count_before + 1)
        # Cleanup
        os.unlink(settings.MEDIA_ROOT + "test.txt")
        os.unlink(settings.MEDIA_ROOT + "test2.txt")
