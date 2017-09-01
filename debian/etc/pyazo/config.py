"""
Supervisr default local settings
"""
from os import path

from pyazo.utils import db_settings_from_dbconfig

LOCAL_BASE = path.join((path.dirname(__file__)) + '/')

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
