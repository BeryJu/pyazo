"""
Pyazo Reindex management command
"""

import hashlib
import logging
from glob import glob

from django.conf import settings
from django.core.management.base import BaseCommand

from pyazo.models import Upload

BUF_SIZE = 65536
LOGGER = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Turns maintenance Mode on or off via manage.py
    """

    help = "Reindex Images in '%s'" % settings.MEDIA_ROOT

    @staticmethod
    def _file_get_sha_512(path):
        sha512 = hashlib.sha512()
        with open(path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha512.update(data)
        return sha512.hexdigest()

    def handle(self, *args, **options):
        files = glob(settings.MEDIA_ROOT + '**')
        for file in files:
            # Get hash to compare with
            sha512 = Command._file_get_sha_512(file)
            # Check if that hash exists
            matching = Upload.objects.filter(sha512=sha512)
            if matching.exists():
                LOGGER.info("File %s is in DB already", file)
            else:
                Upload.objects.create(
                    file=file, type=0)
                LOGGER.info("Imported %s into DB", file)
