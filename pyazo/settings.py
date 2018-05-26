"""
Django settings for pyazo project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import importlib
import logging
import os
import subprocess
import sys

import raven

LOGGER = logging.getLogger(__name__)



# This is the base url used for image URLs
EXTERNAL_URL = 'http://localhost:8000'
# This dictates how the Path is generated
# can be either of:
# - view_sha512_short
# - view_md5
# - view_sha256
# - view_sha512
DEFAULT_RETURN_VIEW = 'view_sha256'
# Set this to true if you only want to use external authentication
EXTERNAL_AUTH_ONLY = False
# If this is true, images are automatically claimed if the windows user exists
# in django
AUTO_CLAIM_ENABLED = True


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '48e9z8tw=_z0e#m*x70&)u%cgo8#=16uzdze&i8q=*#**)@cp&' # noqa Debug SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

LOGIN_REDIRECT_URL = 'index'
# Application definition
LOGOUT_REDIRECT_URL = 'accounts_login'

CHERRYPY_SERVER = {
    'socket_host': '0.0.0.0',
    'socket_port': 8000,
    'thread_pool': 30
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth_supervisr',
    'pyazo',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
]

ROOT_URLCONF = 'pyazo.urls'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'pyazo/templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

VERSION = 'dev'
try:
    VERSION = subprocess.check_output(['dpkg-query', "--showformat='${Version}'",
                                       '--show', 'pyazo']).decode('utf-8')[1:-1]
except Exception: # pylint: disable=broad-except
    VERSION = raven.fetch_git_sha(os.path.dirname(os.pardir))
ERROR_REPORT_ENABLED = False

WSGI_APPLICATION = 'pyazo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

LOG_LEVEL_FILE = 'DEBUG'
LOG_FILE = '/dev/null'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
sys.path.append('/etc/pyazo')

def load_local_settings(mod):
    """Load module *mod* and apply contents to ourselves"""
    try:
        loaded_module = importlib.import_module(mod, package=None)
        for key, val in loaded_module.__dict__.items():
            if not key.startswith('__') and not key.endswith('__'):
                globals()[key] = val
        LOGGER.warning("Loaded '%s' as local_settings", mod)
        return True
    except ImportError as exception:
        LOGGER.info('Not loaded %s because %s', mod, exception)
        return False
    except PermissionError:
        return False

for modu in [os.environ.get('PYAZO_LOCAL_SETTINGS', 'pyazo.local_settings'), 'config']:
    if load_local_settings(modu):
        break

if ERROR_REPORT_ENABLED:
    INSTALLED_APPS += ['raven.contrib.django.raven_compat']

RAVEN_CONFIG = {
    'dsn': 'https://dfcc6acbd9c543ea8d4c9dbf4ac9a8c0:5340ca78902841b5b'
           '3372ecce5d548a5@sentry.services.beryju.org/4',
    'release': VERSION,
    'environment': 'production' if DEBUG is False else 'development',
    'tags': {'external_domain': EXTERNAL_URL}
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': ('[%(asctime)s] %(levelname)s '
                       '[%(name)s::%(funcName)s::%(lineno)s] %(message)s'),
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'file': {
            'level': LOG_LEVEL_FILE,
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': LOG_FILE,
        },
    },
    'loggers': {
        'pyazo': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'allauth': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cherrypy': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
