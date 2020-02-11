"""pyazo API Urls"""
from django.conf.urls import url
from django.urls import path
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from pyazo.api.viewsets import (
    CollectionViewSet,
    ObjectViewsSet,
    ObjectViewViewSet,
    UserViewSet,
)

ROUTER = DefaultRouter()
ROUTER.register("objects", ObjectViewsSet)
ROUTER.register("object_views", ObjectViewViewSet)
ROUTER.register("collections", CollectionViewSet)
ROUTER.register("users", UserViewSet)


info = openapi.Info(
    title="pyazo API",
    default_version="v2",
    contact=openapi.Contact(email="hello@beryju.org"),
    license=openapi.License(name="MIT License"),
)
SchemaView = get_schema_view(info, public=True,)

urlpatterns = [
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        SchemaView.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        SchemaView.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", SchemaView.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + ROUTER.urls
