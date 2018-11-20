"""test tasks"""
import glob
import os

from django.conf import settings
from django.test import TestCase

from pyazo.models import Upload
from pyazo.tasks import make_thumbnail


class TaskTests(TestCase):
    """Test tasks"""

    def setUp(self):
        super().setUp()
        with open(settings.MEDIA_ROOT + 'test2.txt', 'w') as _file:
            _file.write('updating existing upload')
        self.upload = Upload.objects.create(file=settings.MEDIA_ROOT + 'test2.txt')

    def tearDown(self):
        super().tearDown()
        os.unlink(settings.MEDIA_ROOT + 'test2.txt')
        # delete all files generated by uploads
        for file in glob.glob(settings.MEDIA_ROOT + '*txt'):
            os.remove(file)

    def test_make_thumbnail(self):
        """test make_thumbnail"""
        # pylint gets confused by celery tasks
        make_thumbnail(self.upload.pk) # pylint: disable=no-value-for-parameter
