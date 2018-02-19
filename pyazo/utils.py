"""
pyazo utils
"""

import os
import socket
import zipfile
from io import BytesIO

from django.http import HttpResponse


def get_remote_ip(req):
    """
    Return the remote's IP
    """
    if not req:
        return '0.0.0.0'
    if req.META.get('HTTP_X_FORWARDED_FOR'):
        return req.META.get('HTTP_X_FORWARDED_FOR')
    return req.META.get('REMOTE_ADDR')

def get_reverse_dns(dev_ip):
    """
    Does a reverse DNS lookup and returns the first IP
    """
    try:
        rev = socket.gethostbyaddr(dev_ip)
        if rev:
            return rev[0]
        return ''
    except (socket.herror, socket.gaierror, TypeError, IndexError):
        return ''

def db_settings_from_dbconfig(config_path):
    """
    Generate Django DATABASE dict from dbconfig file
    """
    db_config = {}
    with open(config_path, 'r') as file:
        contents = file.read().split('\n')
        for line in contents:
            if line.startswith('#') or line == '':
                continue
            key, value = line.split('=')
            value = value[1:-1]
            if key == 'dbuser':
                db_config['USER'] = value
            elif key == 'dbpass':
                db_config['PASSWORD'] = value
            elif key == 'dbname':
                db_config['NAME'] = value
            elif key == 'dbserver':
                db_config['HOST'] = value
            elif key == 'dbport':
                db_config['PORT'] = value
            elif key == 'dbtype':
                if value == 'mysql':
                    db_config['ENGINE'] = 'django.db.backends.mysql'
                    db_config['OPTIONS'] = {
                        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
                    }
                elif value == 'pgsql':
                    db_config['ENGINE'] = 'django.db.backends.postgresql'
        return db_config

def read_simple(path, mode='r'):
    """
    Simple wrapper for file reading
    """
    with open(path, mode) as file:
        return file.read()

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
            if os.path.isfile(filename): # regular files only
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
