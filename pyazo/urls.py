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
    url(r'^gyazo\.php$', core.upload_legacy, name='core-upload_legacy'),
    url(r'^(?P<hash>\w{32})\.png$', core.view_md5, name='core-view_md5'),
    url(r'^(?P<hash>\w{64})\.png$', core.view_sha256, name='core-view_sha256'),
    url(r'^(?P<hash>\w{128})\.png$', core.view_sha512, name='core-view_sha512'),
    url(r'^w/thumb/(?P<hash>\w{128})\.png$', core.thumb_view_sha512, name='core-thumb-view_sha512'),
]

