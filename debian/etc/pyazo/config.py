"""
pyazo default local settings
"""
from os import path

from pyazo.utils import db_settings_from_dbconfig

LOCAL_BASE = path.join((path.dirname(__file__)) + '/')

# Set this to the server's external address.
# This is used to generate external URLs
EXTERNAL_URL = 'test.example.log'

# This dictates how the Path is generated
# can be either of:
# - view_sha512_short
# - view_md5
# - view_sha256
# - view_sha512
DEFAULT_RETURN_VIEW = 'view_sha256'

# Set this to this server's hostname or the external domain as if behind a reverse proxy
ALLOWED_HOSTS = ['test.example.org']

# Set this to true if you only want to use external authentication
EXTERNAL_AUTH_ONLY = False

# Enable Error Reporting (Sends error to sentry.services.beryju.org)
ERROR_REPORT_ENABLED = False

DEBUG = False

CHERRYPY_SERVER = {
    'socket_host': '0.0.0.0',
    'socket_port': 8000,
    'thread_pool': 30
}

# Never share this key with anyone.
# If you change this key, you also have to clear your database otherwise things break.
SECRET_KEY = ''
with open(path.join(LOCAL_BASE, 'secret_key'), 'r') as f:
    SECRET_KEY = f.read()

LOG_LEVEL_CONSOLE = 'WARNING'
LOG_LEVEL_FILE = 'INFO'
LOG_FILE = '/var/log/pyazo/pyazo.log'

DATABASES = {
    'default': db_settings_from_dbconfig(path.join(LOCAL_BASE, 'database-config')),
}
