"""pyazo download views"""
import copy
import logging
import os.path
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse

LOGGER = logging.getLogger(__name__)
SXCU_BASE = {
    'Name': 'Pyazo %s',
    'DestinationType': 'ImageUploader',
    'RequestURL': '%s://%s/upload/',
    'FileFormName': 'imagedata',
    'Arguments': {
        'id': '%rn',
        'username': '%uln',
    }
}


@login_required
def client_windows(request: HttpRequest) -> HttpResponse:
    """Download Client (Windows)"""
    client_path = os.path.join(settings.BASE_DIR+"/", 'bin/', 'Pyazo.exe')
    host = urlparse(request.build_absolute_uri()).netloc
    filename = "Pyazo_%s.exe" % host
    if os.path.isfile(client_path):
        with open(client_path, 'rb') as _file:
            response = HttpResponse(
                _file.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=%s' % filename
            return response
    raise Http404


@login_required
def sxcu(request: HttpRequest) -> HttpResponse:
    """Download ShareX Custom Uploader"""
    url = urlparse(request.build_absolute_uri())
    data = copy.deepcopy(SXCU_BASE)
    scheme = 'https' if request.is_secure() else 'http'
    data['RequestURL'] = data['RequestURL'] % (scheme, url.netloc)
    data['Name'] = data['Name'] % url.netloc
    response = JsonResponse(data)
    response['Content-Disposition'] = 'attachment; filename=pyazo.sxcu'
    return response


@login_required
def client_macos(request: HttpRequest) -> HttpResponse:
    """Download Client (macOS)"""
    client_path = os.path.join(settings.BASE_DIR+"/", 'bin/', 'pyazo.dmg')
    if os.path.isfile(client_path):
        with open(client_path, 'rb') as _file:
            response = HttpResponse(
                _file.read(), content_type="application/x-apple-diskimage")
            response['Content-Disposition'] = 'inline; filename=pyazo.dmg'
            return response
    raise Http404
