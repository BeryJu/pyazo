"""pyazo URL Configuration"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.urls import path

from pyazo.views import accounts, core, download, upload, view

admin.site.index_title = 'Pyazo Admin'
admin.site.site_title = 'pyazo'

urlpatterns = [
    url(r'^$', core.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/allauth/', include('allauth.urls')),
    url(r'^accounts/login/$', accounts.login, name='accounts-login'),
    url(r'^accounts/logout/$', accounts.logout, name='accounts-logout'),
    url(r'^download/win/$', download.client_windows, name='download_client_windows'),
    url(r'^download/sharex/$', download.sxcu, name='download-sxcu'),
    url(r'^download/macos/$', download.client_macos, name='download_client_macos'),
    url(r'^gyazo\.php$', upload.upload, name='upload'),
    url(r'^upload/$', upload.upload, name='upload'),
    url(r'^upload/browser/$', upload.upload_browser, name='upload_browser'),
    url(r'^upload/(?P<file_hash>\w{128})/view/$', upload.view, name='upload_view'),
    url(r'^upload/(?P<file_hash>\w{128})/claim/$', upload.claim, name='upload_claim'),
    url(r'^(?P<file_hash>\w{16})$', view.view_sha512_short, name='view_sha512_short'),
    url(r'^(?P<file_hash>\w{32})$', view.view_md5, name='view_md5'),
    url(r'^(?P<file_hash>\w{64})$', view.view_sha256, name='view_sha256'),
    url(r'^(?P<file_hash>\w{128})$', view.view_sha512, name='view_sha512'),
    url(r'^(?P<file_hash>\w{16})\.png$', view.view_sha512_short, name='view_sha512_short'),
    url(r'^(?P<file_hash>\w{32})\.png$', view.view_md5, name='view_md5'),
    url(r'^(?P<file_hash>\w{64})\.png$', view.view_sha256, name='view_sha256'),
    url(r'^(?P<file_hash>\w{128})\.png$', view.view_sha512, name='view_sha512'),
    url(r'^w/thumb/(?P<file_hash>\w{128})\.png$', view.thumb_view_sha512, name='thumb-view_sha512'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
