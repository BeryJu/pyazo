"""pyazo download views"""
import copy
import logging
import os.path
import re
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse

from pyazo.utils import zip_to_response

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
    data['RequestURL'] = data['RequestURL'] % (url.scheme, url.netloc)
    data['Name'] = data['Name'] % url.netloc
    response = JsonResponse(data)
    response['Content-Disposition'] = 'attachment; filename=pyazo.sxcu'
    return response


@login_required
def client_macos(request: HttpRequest) -> HttpResponse:
    """Download zipped macos client"""
    # First we replace the `SERVER` line
    uri = urlparse(request.build_absolute_uri())
    # Try to take port from URI, otherwise fall back to standard ports
    port = 443 if not uri.port else uri.port
    # replace text in script file
    app_path = os.path.join(settings.BASE_DIR+"/", 'bin/', 'Pyazo.app/')
    script_file = os.path.join(app_path, "Contents/Resources/script")
    regex_replace = {
        r"^HOST\s=\s'(.*)'$": "HOST = '%s'" % uri.hostname,
        r"^PORT\s=\s\d+$": "PORT = %d" % port,
        r"use_ssl\s=>\s\w{4,5}": "use_ssl => %s" % ('true'
                                                    if uri.scheme == 'https' else 'false'),
    }
    try:
        inp = open(script_file, 'r')
        data = inp.read()
        inp.close()
        for regex, repl in regex_replace.items():
            data = re.sub(regex, repl, data, flags=re.M)
        with open(script_file, 'w') as out:
            out.write(data)
        return zip_to_response(app_path, 'Pyazo.app.zip')
    except IOError as exc:
        LOGGER.warning(exc)
        raise Http404
