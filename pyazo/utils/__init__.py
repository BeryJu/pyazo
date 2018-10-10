"""pyazo utils"""

import os
import socket
import zipfile
from io import BytesIO
import magic

from django.http import HttpResponse, HttpRequest


def get_remote_ip(request: HttpRequest) -> str:
    """Return the remote's IP"""
    if not request:
        return '0.0.0.0'
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        return request.META.get('HTTP_X_FORWARDED_FOR')
    return request.META.get('REMOTE_ADDR')

def get_mime_type(file_path: str) -> str:
    """Return mime-type for file"""
    return magic.from_file(file_path, mime=True)

def get_reverse_dns(ipaddress: str) -> str:
    """Does a reverse DNS lookup and returns the first IP"""
    try:
        rev = socket.gethostbyaddr(ipaddress)
        if rev:
            return rev[0]
        return ''
    except (socket.herror, socket.gaierror, TypeError, IndexError):
        return ''


def zip_to_response(folder: str, archive_name: str) -> HttpResponse:
    """Zip a folder and return a HTTP Response as download"""
    # Open StringIO to grab in-memory ZIP contents
    tmp_file = BytesIO()
    zip_file = zipfile.ZipFile(tmp_file, "w")

    relroot = os.path.abspath(os.path.join(folder, os.pardir))
    for root, _dirs, files in os.walk(folder):
        # add directory (needed for empty dirs)
        zip_file.write(root, os.path.relpath(root, relroot))
        for file in files:
            filename = os.path.join(root, file)
            if os.path.isfile(filename):  # regular files only
                arcname = os.path.join(os.path.relpath(root, relroot), file)
                zip_file.write(filename, arcname)

    # Must close zip for all contents to be written
    zip_file.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(tmp_file.getvalue(),
                        content_type="application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % archive_name

    return resp
