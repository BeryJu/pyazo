"""pyazo download views"""
from logging import getLogger
import os.path
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.views.generic import View

LOGGER = getLogger(__name__)


class ClientDownloadView(LoginRequiredMixin, View):
    """View to download clients"""

    def get(self, request: HttpRequest, client: str) -> HttpResponse:
        """Proxy request to fitting method"""
        client_names = {
            'windows': self.client_windows,
            'sharex': self.client_share_x,
            'macos': self.client_mac_os,
        }
        if client in client_names:
            return client_names[client](request)
        raise Http404

    def client_windows(self, request: HttpRequest) -> HttpResponse:
        """Download windows client"""
        client_path = os.path.join(settings.BASE_DIR+"/", 'bin/', 'Pyazo.exe')
        host = urlparse(request.build_absolute_uri()).netloc
        filename = "Pyazo_%s.exe" % host
        if os.path.isfile(client_path):
            with open(client_path, 'rb') as _file:
                response = HttpResponse(
                    _file.read(), content_type="application/octet-stream")
                response['Content-Disposition'] = 'inline; filename=%s' % filename
                return response
        else:
            LOGGER.warning("File %s not found", client_path)
        raise Http404

    def client_share_x(self, request: HttpRequest) -> HttpResponse:
        """Download ShareX custom uploader"""
        data = {
            'Name': 'Pyazo %s',
            'DestinationType': 'ImageUploader',
            'RequestURL': '%s://%s/upload/',
            'FileFormName': 'imagedata',
            'Arguments': {
                'id': '%rn',
                'username': '%uln',
            }
        }
        url = urlparse(request.build_absolute_uri())
        scheme = 'https' if request.is_secure() else 'http'
        data['RequestURL'] = data['RequestURL'] % (scheme, url.netloc)
        data['Name'] = data['Name'] % url.netloc
        response = JsonResponse(data)
        response['Content-Disposition'] = 'attachment; filename=pyazo.sxcu'
        return response

    def client_mac_os(self, request: HttpRequest) -> HttpResponse:
        """Download Client (macOS)"""
        client_path = os.path.join(settings.BASE_DIR+"/", 'bin/', 'pyazo.dmg')
        if os.path.isfile(client_path):
            with open(client_path, 'rb') as _file:
                response = HttpResponse(
                    _file.read(), content_type="application/x-apple-diskimage")
                response['Content-Disposition'] = 'inline; filename=pyazo.dmg'
                return response
        else:
            LOGGER.warning("File %s not found", client_path)
        raise Http404
