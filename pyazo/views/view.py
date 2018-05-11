"""pyazo viewing views"""
import logging

import magic
from django.http import Http404, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control

from pyazo.models import Upload, UploadView
from pyazo.utils import get_remote_ip, get_reverse_dns

LOGGER = logging.getLogger(__name__)

def handle_view(request: HttpRequest, uploads) -> HttpResponse:
    """Show uploads"""
    if uploads.exists():
        upload = uploads.first()
        client_ip = get_remote_ip(request)
        client_dns = get_reverse_dns(client_ip)
        user_agent = request.META['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in request.META else ''
        UploadView.objects.create(
            upload=upload,
            viewee_ip=client_ip,
            viewee_dns=client_dns,
            viewee_user_agent=user_agent
            )
        LOGGER.info("Logged view for %s (%s) viewing '%s'", client_ip, client_dns, upload.md5)
        content_type = magic.from_file(upload.file.name, mime=True)
        return HttpResponse(upload.file.read(), content_type=content_type)
    raise Http404

@cache_control(max_age=3600)
def view_md5(request: HttpRequest, file_hash) -> HttpResponse:
    """Search upload by md5 and return it"""
    uploads = Upload.objects.filter(md5=file_hash)
    return handle_view(request, uploads)

@cache_control(max_age=3600)
def view_sha256(request: HttpRequest, file_hash) -> HttpResponse:
    """Search upload by sha256 and return it"""
    uploads = Upload.objects.filter(sha256=file_hash)
    return handle_view(request, uploads)

@cache_control(max_age=3600)
def view_sha512(request: HttpRequest, file_hash) -> HttpResponse:
    """Search upload by sha512 and return it"""
    uploads = Upload.objects.filter(sha512=file_hash)
    return handle_view(request, uploads)

@cache_control(max_age=3600)
def view_sha512_short(request: HttpRequest, file_hash) -> HttpResponse:
    """Search upload by shortened sha512 and return it"""
    uploads = Upload.objects.filter(sha512__startswith=file_hash)
    return handle_view(request, uploads)

@cache_control(max_age=3600)
# pylint: disable=unused-argument
def thumb_view_sha512(request: HttpRequest, file_hash) -> HttpResponse:
    """Search upload by sha512 and return it (don't log it tho)"""
    uploads = Upload.objects.filter(sha512=file_hash)
    if uploads.exists():
        upload = uploads.first()
        return HttpResponse(upload.file.read(), content_type="image/png")
    raise Http404
