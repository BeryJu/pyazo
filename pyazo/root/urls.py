"""pyazo URL Configuration"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views
from django.urls import include, path
from django.views.generic.base import RedirectView

from pyazo.core.views import auth, clients, core, upload, view

admin.site.index_title = "pyazo Admin"
admin.site.site_title = "pyazo"

urlpatterns = [
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("", RedirectView.as_view(url="overview/")),
    path("api/v2/", include("pyazo.api.urls")),
    path("overview/", core.IndexView.as_view(), name="index"),
    path("admin/", admin.site.urls),
    path("accounts/login/", auth.CustomLoginView.as_view(), name="accounts-login"),
    path("accounts/logout/", views.LogoutView.as_view(), name="accounts-logout"),
    path(
        "download/<slug:client>/",
        clients.ClientDownloadView.as_view(),
        name="download-client",
    ),
    # Legacy upload URL
    path("gyazo.php", upload.LegacyObjectView.as_view(), name="upload"),
    path("upload/", upload.LegacyObjectView.as_view(), name="upload"),
    path("upload/browser/", upload.BrowserObjectView.as_view(), name="upload_browser"),
    url(
        r"^upload/(?P<file_hash>\w{128})/view/$",
        upload.ObjectView.as_view(),
        name="upload_view",
    ),
    url(
        r"^upload/(?P<file_hash>\w{128})/claim/$",
        upload.ClaimObjectView.as_view(),
        name="upload_claim",
    ),
    url(
        r"^upload/(?P<file_hash>\w{128})/delete/$",
        upload.DeleteObjectView.as_view(),
        name="upload_delete",
    ),
    # All view URLs are handeled by the same Function, but we need different names
    # so the default can be changed in the settings
    url(
        r"^(?P<file_hash>\w{16})(\..{1,5})?$",
        view.ObjectViewFile.as_view(),
        name="view_sha512_short",
    ),
    url(
        r"^(?P<file_hash>\w{32})(\..{1,5})?$",
        view.ObjectViewFile.as_view(),
        name="view_md5",
    ),
    url(
        r"^(?P<file_hash>\w{64})(\..{1,5})?$",
        view.ObjectViewFile.as_view(),
        name="view_sha256",
    ),
    url(
        r"^(?P<file_hash>\w{128})(\..{1,5})?$",
        view.ObjectViewFile.as_view(),
        name="view_sha512",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
