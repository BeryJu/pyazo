"""test management commands"""
import os

from django.conf import settings
from django.test import TestCase

from pyazo.core.management.commands.reindex import Command as ReindexCommand
from pyazo.core.models import Object
from pyazo.core.tests.utils import call_command_ret


class ManagementTests(TestCase):
    """Test django management commands"""

    def test_reindex(self):
        """Test reindex command"""
        with open(settings.MEDIA_ROOT + "test.txt", "w") as _file:
            _file.write("test")
        with open(settings.MEDIA_ROOT + "test2.txt", "w") as _file:
            _file.write("updating existing upload")
        Object.objects.create(file=settings.MEDIA_ROOT + "test2.txt")
        count_before = len(Object.objects.all())
        self.assertEqual(ReindexCommand().handle(), 0)
        # We expect reindex to create one new upload
        self.assertEqual(len(Object.objects.all()), count_before + 1)
        # Cleanup
        os.unlink(settings.MEDIA_ROOT + "test.txt")
        os.unlink(settings.MEDIA_ROOT + "test2.txt")

    def test_generate_secret_key(self):
        """Test generate_secret_key"""
        self.assertEqual(len(call_command_ret("generate_secret_key")), 51)
