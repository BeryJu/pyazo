"""
Django settings for pyazo project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from json import dumps
import os
import sys

import structlog
from sentry_sdk import init as sentry_init
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

from pyazo import __version__
from pyazo.utils.config import CONFIG
from pyazo.utils.sentry import before_send


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.y(
    "secret_key", "48e9z8tw=_z0e#m*x70&)u%cgo8#=16uzdze&i8q=*#**)@cp&"
)  # noqa Debug

DEBUG = CONFIG.y("debug")

# Also allow server's hostname and server's fqdn
ALLOWED_HOSTS = ["*"]

# Application definition
LOGIN_URL = "accounts-login"
LOGIN_REDIRECT_URL = "/overview/"
LOGOUT_REDIRECT_URL = "accounts-login"
INTERNAL_IPS = ["127.0.0.1"]

# Redis settings
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": (
            f"redis://:{CONFIG.y('redis.password')}@{CONFIG.y('redis.host')}:6379"
            f"/{CONFIG.y('redis.cache_db')}"
        ),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
DJANGO_REDIS_IGNORE_EXCEPTIONS = True
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Celery settings
# Add a 10 minute timeout to all Celery tasks.
CELERY_TASK_SOFT_TIME_LIMIT = 600
CELERY_CREATE_MISSING_QUEUES = True
CELERY_TASK_DEFAULT_QUEUE = "pyazo"
CELERY_BROKER_URL = (
    f"redis://:{CONFIG.y('redis.password')}@{CONFIG.y('redis.host')}"
    f":6379/{CONFIG.y('redis.message_queue_db')}"
)
CELERY_RESULT_BACKEND = (
    f"redis://:{CONFIG.y('redis.password')}@{CONFIG.y('redis.host')}"
    f":6379/{CONFIG.y('redis.message_queue_db')}"
)

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# OIDC settings
if CONFIG.y("oidc.client_id", None):
    OIDC_RP_CLIENT_ID = CONFIG.y("oidc.client_id")
    OIDC_RP_CLIENT_SECRET = CONFIG.y("oidc.client_secret")
    OIDC_OP_AUTHORIZATION_ENDPOINT = CONFIG.y("oidc.authorization_url")
    OIDC_OP_TOKEN_ENDPOINT = CONFIG.y("oidc.token_url")
    OIDC_OP_USER_ENDPOINT = CONFIG.y("oidc.user_url")
    OIDC_OP_JWKS_ENDPOINT = CONFIG.y("oidc.jwks_url")
    OIDC_RP_SIGN_ALGO = CONFIG.y("oidc.algo", "RS256")
    OIDC_USERNAME_ALGO = "pyazo.root.auth.generate_username"
    AUTHENTICATION_BACKENDS += [
        "pyazo.root.auth.IDTokenOIDC",
    ]
    print(dumps({"event": "OIDC Enabled.", "level": "info", "logger": __name__}))

# LDAP Settings
if CONFIG.y_bool("ldap.enabled"):
    from django_auth_ldap.config import LDAPSearch

    AUTH_LDAP_SERVER_URI = CONFIG.y("ldap.server.uri")
    AUTH_LDAP_START_TLS = CONFIG.y_bool("ldap.server.tls")
    AUTH_LDAP_BIND_DN = CONFIG.y("ldap.bind.dn")
    AUTH_LDAP_BIND_PASSWORD = CONFIG.y("ldap.bind.password")
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        CONFIG.y("ldap.search_base"),
        2,
        CONFIG.y("ldap.filter", "(sAMAccountName=%(user)s)"),
    )
    AUTHENTICATION_BACKENDS += [
        "django_auth_ldap.backend.LDAPBackend",
    ]
    if CONFIG.y("ldap.require_group", None):
        AUTH_LDAP_REQUIRE_GROUP = CONFIG.y("ldap.require_group")
    print(dumps({"event": "LDAP Enabled.", "level": "info", "logger": __name__}))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "mozilla_django_oidc",
    "pyazo.core.apps.PyazoCoreConfig",
    "pyazo.api.apps.PyazoAPIConfig",
    "rest_framework",
    "drf_yasg",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pyazo.root.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "pyazo/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

VERSION = __version__

ASGI_APPLICATION = "pyazo.root.asgi.application"

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": CONFIG.y("postgresql.host"),
        "NAME": CONFIG.y("postgresql.name"),
        "USER": CONFIG.y("postgresql.user"),
        "PASSWORD": CONFIG.y("postgresql.password"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = "/static/"


# Sentry integration
_ERROR_REPORTING = CONFIG.y_bool("error_reporting", False)
if not DEBUG and _ERROR_REPORTING:
    sentry_init(
        dsn="https://57bd7622b7114f1d87315dbe4f5b0488@sentry.beryju.org/5",
        integrations=[
            DjangoIntegration(transaction_style="function_name"),
            CeleryIntegration(),
        ],
        before_send=before_send,
        release="pyazo@%s" % __version__,
        traces_sample_rate=1.0,
        send_default_pii=False,
    )
    print(
        dumps(
            {
                "event": "Error reporting is enabled.",
                "level": "info",
                "logger": __name__,
            }
        )
    )


structlog.configure_once(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(),
        structlog.processors.StackInfoRenderer(),
        # structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

LOG_PRE_CHAIN = [
    # Add the log level and a timestamp to the event_dict if the log entry
    # is not from structlog.
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
    structlog.processors.TimeStamper(),
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(sort_keys=True),
            "foreign_pre_chain": LOG_PRE_CHAIN,
        },
        "colored": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(colors=DEBUG),
            "foreign_pre_chain": LOG_PRE_CHAIN,
        },
    },
    "handlers": {
        "console": {
            "level": DEBUG,
            "class": "logging.StreamHandler",
            "formatter": "colored" if DEBUG else "plain",
        },
    },
    "loggers": {},
}
_LOGGING_HANDLER_MAP = {
    "": "DEBUG",
    "pyazo": "DEBUG",
    "django": "WARNING",
    "celery": "WARNING",
    "oauthlib": "DEBUG",
    "mozilla_django_oidc": "DEBUG",
    "django_auth_ldap": "DEBUG",
}
for handler_name, level in _LOGGING_HANDLER_MAP.items():
    LOGGING["loggers"][handler_name] = {
        "handlers": ["console"],
        "level": level,
        "propagate": False,
    }


TEST = any("test" in arg for arg in sys.argv)
TEST_RUNNER = "xmlrunner.extra.djangotestrunner.XMLTestRunner"
TEST_OUTPUT_VERBOSE = 2

TEST_OUTPUT_FILE_NAME = "unittest.xml"

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
THUMBNAIL_ROOT = os.path.join(BASE_DIR, "media/thumbnail/")

if TEST:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
    }
    CELERY_TASK_ALWAYS_EAGER = True
    MEDIA_ROOT = os.path.join(BASE_DIR, "media_test/")
    THUMBNAIL_ROOT = os.path.join(BASE_DIR, "media_test/thumbnail/")

os.makedirs(MEDIA_ROOT, exist_ok=True)
os.makedirs(THUMBNAIL_ROOT, exist_ok=True)

if DEBUG is True:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
