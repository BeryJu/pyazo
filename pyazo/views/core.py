
import logging
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth.decorators import login_required
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
def upload_legacy(req):
    if 'id' in req.POST and 'imagedata' in req.FILES:
        client_ip = get_remote_ip(req)
        client_dns = get_reverse_dns(client_ip)

        file = save_from_post(req.FILES['imagedata'].read())

        new_upload = Upload(
            file=file,
            type=0)
        new_upload.save()

        new_upload_view = UploadView(
            upload=new_upload,
            viewee_ip=client_ip,
            viewee_dns=client_dns,
            viewee_user_agent=req.META['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in req.META else ''
            )
        new_upload_view.save()

        print( "Uploaded %s from %s" % (new_upload.filename, client_ip))

        # Generate url for client to open
        url = reverse('core-view_sha256', kwargs={ 'hash': new_upload.sha256 })
        full_url = urljoin(settings.EXTERNAL_URL, url)
        return HttpResponse(url)
    else:
        return HttpResponse(status=400)

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
    else:
        return Http404

def view_md5(req, hash):
    """
    Search upload by md5 and return it
    """
    uploads = Upload.objects.filter(md5=hash)
    return handle_view(req, uploads)

def view_sha256(req, hash):
    """
    Search upload by sha256 and return it
    """
    uploads = Upload.objects.filter(sha256=hash)
    return handle_view(req, uploads)

def view_sha512(req, hash):
    """
    Search upload by sha512 and return it
    """
    uploads = Upload.objects.filter(sha512=hash)
    return handle_view(req, uploads)

def thumb_view_sha512(req, hash):
    """
    Search upload by sha512 and return it (don't log it tho)
    """
    uploads = Upload.objects.filter(sha512=hash)
    if uploads.exists():
        upload = uploads.first()
        return HttpResponse(upload.file.read(), content_type="image/png")
    else:
        return Http404
