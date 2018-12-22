"""pyazo API Urls"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from pyazo.api.viewsets import (CollectionViewSet, ObjectViewsSet,
                                ObjectViewViewSet, UserViewSet)

ROUTER = DefaultRouter()
ROUTER.register('objects', ObjectViewsSet)
ROUTER.register('object_views', ObjectViewViewSet)
ROUTER.register('collections', CollectionViewSet)
ROUTER.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(ROUTER.urls)),
    path('swagger/', get_swagger_view(title='pyazo API'))
]
