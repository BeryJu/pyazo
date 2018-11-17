"""pyazo tasks"""
import os
from logging import getLogger

from django.conf import settings
from django.shortcuts import get_object_or_404
from PIL import Image

from pyazo.celery import CELERY_APP
from pyazo.models import Upload
from pyazo.utils.files import generate_ext_thumb

LOGGER = getLogger(__name__)

@CELERY_APP.task(bind=True)
# pylint: disable=unused-argument
def make_thumbnail(self, upload_pk: int):
    """Create 200x200 thumbnail for upload.
    If upload is non-image, return thumbnail with filetype"""
    path = ''
    upload = get_object_or_404(Upload, pk=upload_pk)
    if upload.mime_type.startswith('image/'):
        LOGGER.debug('Creating thumbnail of upload...')
        # Upload is an image, so we create a resized version
        img = Image.open(upload.file)
        img.thumbnail((200, 200))
        thumb_path = settings.THUMBNAIL_ROOT + upload.sha512 + '_thumb.png'
        img.save(thumb_path)
        # FileField's path needs to be relative to MEDIA_ROOT, so we remove MEDIA_ROOT
        path = thumb_path.replace(settings.MEDIA_ROOT, '')
    else:
        LOGGER.debug('Assigning thumbnail of extension...')
        # Upload is another file, so we create a filetype thumbnail
        _, ext = os.path.splitext(upload.file.name)
        # Prevent file being named `.png` so we rename empty extensions to `empty.png`
        if ext == '':
            ext = '.empty'
        # ext still has a leading dot, which we don't want for saving
        out_name = ext[1:]
        path = settings.THUMBNAIL_ROOT + out_name + '.png'
        # Extension thumb doesn't exist, so we generate thumbnail first
        if not os.path.exists(path):
            generate_ext_thumb(ext)
    upload.thumbnail.name = path
    upload.save()
