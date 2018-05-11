"""supervisr provider"""
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from allauth_supervisr.provider import SupervisrProvider

urlpatterns = default_urlpatterns(SupervisrProvider)
