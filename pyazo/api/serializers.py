"""pyazo API Serializers"""
from django.contrib.auth.models import User
from django.shortcuts import reverse
from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        ReadOnlyField, SerializerMethodField)

from pyazo.core.models import Collection, Object, ObjectView


class UserSerializer(HyperlinkedModelSerializer):
    """User serializer (show basic information)"""

    class Meta:

        model = User
        fields = ['first_name', 'last_name', 'username']


class ObjectSerializer(HyperlinkedModelSerializer):
    """Object serializer (showing URL to file and thumbnail)"""

    file_url = SerializerMethodField()
    thumbnail_url = SerializerMethodField()
    md5 = ReadOnlyField()
    sha256 = ReadOnlyField()
    sha512 = ReadOnlyField()
    mime_type = ReadOnlyField()

    def get_file_url(self, obj):
        """Build absolute URL based on sha512"""
        return self.context['request'].build_absolute_uri(
            reverse('view_sha512', kwargs={'file_hash': obj.sha512}))

    def get_thumbnail_url(self, obj):
        """Build absolute URL based on sha512"""
        return self.context['request'].build_absolute_uri(
            reverse('view_sha512', kwargs={'file_hash': obj.sha512})+'?thumb')

    class Meta:

        model = Object
        fields = ['file', 'file_url', 'thumbnail_url', 'md5',
                  'sha256', 'sha512', 'collection', 'mime_type']

class ObjectViewSerializer(HyperlinkedModelSerializer):
    """Show basic information about View"""

    class Meta:

        model = ObjectView
        fields = ['obj', 'viewee', 'viewee_ip', 'viewee_dns', 'viewee_date', 'viewee_user_agent']

class CollectionSerializer(HyperlinkedModelSerializer):
    """Collection Serializer"""

    class Meta:

        model = Collection
        fields = ['name', 'owner']
