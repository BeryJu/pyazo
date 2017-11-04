"""
pyazo URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

from pyazo.oauth2 import SupervisrOAuthCallback
from pyazo.views import accounts, core, image

urlpatterns = [
    url(r'^$', core.index, name='core-index'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/callback/(?P<provider>(\w|-)+)/$',
        SupervisrOAuthCallback.as_view(), name='allaccess-callback'),
    url(r'^accounts/login/$', accounts.login, name='core-accounts_login'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('allaccess.urls')),
    url(r'^download/win/$', core.download_client_windows, name='core-download_client_windows'),
    url(r'^gyazo\.php$', core.upload, name='core-upload'),
    url(r'^upload/$', core.upload, name='core-upload'),
    url(r'^image/(?P<file_hash>\w{128})/view/$', image.view, name='core-image_view'),
    url(r'^image/(?P<file_hash>\w{128})/claim/$', image.claim, name='core-image_claim'),
    url(r'^(?P<file_hash>\w{16})\.png$', core.view_sha512_short, name='core-view_sha512_short'),
    url(r'^(?P<file_hash>\w{32})\.png$', core.view_md5, name='core-view_md5'),
    url(r'^(?P<file_hash>\w{64})\.png$', core.view_sha256, name='core-view_sha256'),
    url(r'^(?P<file_hash>\w{128})\.png$', core.view_sha512, name='core-view_sha512'),
    url(r'^w/thumb/(?P<file_hash>\w{128})\.png$', core.thumb_view_sha512,
        name='core-thumb-view_sha512'),
]
