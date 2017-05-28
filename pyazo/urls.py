"""
pyazo URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin
from pyazo.views import core
from pyazo.oauth2 import SupervisrOAuthCallback

urlpatterns = [
    url(r'^$', core.index, name='core-index'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/callback/(?P<provider>(\w|-)+)/$',
        SupervisrOAuthCallback.as_view(), name='allaccess-callback'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('allaccess.urls')),
]

