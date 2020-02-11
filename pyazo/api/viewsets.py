"""pyazo API Viewsets"""
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from pyazo.api.serializers import (
    CollectionSerializer,
    ObjectSerializer,
    ObjectViewSerializer,
    UserSerializer,
)
from pyazo.core.models import Collection, Object, ObjectView


# pylint: disable=too-many-ancestors
class UserViewSet(ModelViewSet):
    """User viewset (only show current user for normal users, otherwise all users)"""

    queryset = User.objects.none()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)


# pylint: disable=too-many-ancestors
class ObjectViewsSet(ModelViewSet):
    """Show all Objects if superuser, otherwise only objects owned by current user"""

    queryset = Object.objects.all()
    serializer_class = ObjectSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Object.objects.all()
        return Object.objects.filter(user=self.request.user.pk)


# pylint: disable=too-many-ancestors
class ObjectViewViewSet(ReadOnlyModelViewSet):
    """Show all Views related"""

    queryset = ObjectView.objects.all()
    serializer_class = ObjectViewSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ObjectView.objects.all()
        return ObjectView.objects.filter(object_user=self.request.user.pk)


# pylint: disable=too-many-ancestors
class CollectionViewSet(ModelViewSet):
    """Show all collections"""

    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Collection.objects.all()
        return Collection.objects.filter(owner=self.request.user.pk)
