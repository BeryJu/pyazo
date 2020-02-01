"""Pyazo Reindex management command"""
import hashlib
import os
from glob import glob

from django.conf import settings
from django.core.management.base import BaseCommand
from structlog import get_logger

from pyazo.core.models import Object

BUF_SIZE = 65536
LOGGER = get_logger(__name__)


class Command(BaseCommand):
    """Reindex Images"""

    help = "Reindex Images in '%s'" % settings.MEDIA_ROOT

    @staticmethod
    def _file_get_sha_512(path):
        sha512 = hashlib.sha512()
        with open(path, "rb") as _file:
            while True:
                data = _file.read(BUF_SIZE)
                if not data:
                    break
                sha512.update(data)
        return sha512.hexdigest()

    def handle(self, *args, **options):
        LOGGER.info("Looking in '%s'...", settings.MEDIA_ROOT)
        files = glob(settings.MEDIA_ROOT + "*")
        for file in files:
            if os.path.isfile(file):
                # Get hash to compare with
                sha512 = Command._file_get_sha_512(file)
                # Check if that hash exists
                matching = Object.objects.filter(sha512=sha512)
                if matching.exists():
                    upload = matching.first()
                    upload.file.name = file
                    upload.save()
                    LOGGER.info("File %s is in DB already, updating path", file)
                else:
                    Object.objects.create(file=file)
                    LOGGER.info("Imported %s into DB", file)
        return 0
