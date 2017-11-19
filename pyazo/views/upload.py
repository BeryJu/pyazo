"""pyazo upload views"""
import logging

from django.db.utils import DataError
from django.shortcuts import render

from pyazo.models import Upload, UploadView, save_from_post
from pyazo.utils import get_remote_ip, get_reverse_dns

LOGGER = logging.getLogger(__name__)

def upload(req):
    """Handle uploads from browser"""
    if req.method == 'POST':
        # do stuff
        for filen in req.FILES:
            client_ip = get_remote_ip(req)
            client_dns = get_reverse_dns(client_ip)

            file = save_from_post(req.FILES[filen].read())

            new_upload = Upload(
                file=file,
                type=0,
                user=req.user)
            new_upload.save()

            try:
                uag = req.META['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in req.META else ''
                new_upload_view = UploadView(
                    upload=new_upload,
                    viewee_ip=client_ip,
                    viewee_dns=client_dns,
                    viewee_user_agent=uag
                    )
                new_upload_view.save()
            except DataError:
                LOGGER.info("Failed to create initial view with rIP '%r'", client_ip)

            LOGGER.info("Uploaded %s from %s", new_upload.filename, client_ip)
    return render(req, 'image/upload.html')
