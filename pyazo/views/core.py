"""
pyazo core views
"""
import logging
import os.path
from urllib.parse import urljoin, urlparse

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.utils import DataError
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from pyazo.models import Upload, UploadView, save_from_post
from pyazo.utils import get_remote_ip, get_reverse_dns

LOGGER = logging.getLogger(__name__)

@login_required
def index(req):
    """
    Show overview of newest images
    """
    images = Upload.objects.all().order_by('-id')[:200]
    return render(req, 'core/index.html', {'images': images})

@csrf_exempt
def upload(req):
    """
    Main upload handler. Fully Gyazo compatible.
    """
    if 'id' in req.POST and 'imagedata' in req.FILES:
        client_ip = get_remote_ip(req)
        client_dns = get_reverse_dns(client_ip)

        file = save_from_post(req.FILES['imagedata'].read())

        new_upload = Upload(
            file=file,
            type=0)
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

        # Generate url for client to open
        url = reverse(settings.DEFAULT_RETURN_VIEW, kwargs={'file_hash': new_upload.sha256})
        full_url = urljoin(settings.EXTERNAL_URL, url)
        return HttpResponse(full_url)
    return HttpResponse(status=400)

@login_required
def download_client_windows(req):
    """
    Download Client (Windows)
    """
    client_path = os.path.join(settings.BASE_DIR+"/", 'bin/', 'Pyazo.exe')
    host = urlparse(req.build_absolute_uri()).netloc
    filename = "Pyazo_%s.exe" % host
    if os.path.isfile(client_path):
        with open(client_path, 'rb') as _file:
            response = HttpResponse(_file.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=%s' % filename
            return response
    raise Http404

def handle_view(req, uploads):
    """
    Show uploads
    """
    if uploads.exists():
        upload = uploads.first()
        client_ip = get_remote_ip(req)
        client_dns = get_reverse_dns(client_ip)
        UploadView.objects.create(
            upload=upload,
            viewee_ip=client_ip,
            viewee_dns=client_dns,
            viewee_user_agent=req.META['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in req.META else ''
            )
        LOGGER.info("Logged view for %s (%s) viewing '%s'", client_ip, client_dns, upload.md5)
        return HttpResponse(upload.file.read(), content_type="image/png")
    return Http404

def view_md5(req, file_hash):
    """
    Search upload by md5 and return it
    """
    uploads = Upload.objects.filter(md5=file_hash)
    return handle_view(req, uploads)

def view_sha256(req, file_hash):
    """
    Search upload by sha256 and return it
    """
    uploads = Upload.objects.filter(sha256=file_hash)
    return handle_view(req, uploads)

def view_sha512(req, file_hash):
    """
    Search upload by sha512 and return it
    """
    uploads = Upload.objects.filter(sha512=file_hash)
    return handle_view(req, uploads)

def view_sha512_short(req, file_hash):
    """
    Search upload by shortened sha512 and return it
    """
    uploads = Upload.objects.filter(sha512__startswith=file_hash)
    return handle_view(req, uploads)

# pylint: disable=unused-argument
def thumb_view_sha512(req, file_hash):
    """
    Search upload by sha512 and return it (don't log it tho)
    """
    uploads = Upload.objects.filter(sha512=file_hash)
    if uploads.exists():
        upload = uploads.first()
        return HttpResponse(upload.file.read(), content_type="image/png")
    return Http404
