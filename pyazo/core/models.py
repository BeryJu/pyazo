"""pyazo models"""

from django.contrib.auth.models import User
from django.db import models
from user_agents import parse

from pyazo.utils.files import generate_hashes, get_mime_type


class Object(models.Model):
    """Store data about a single obj"""

    file = models.FileField(max_length=512)
    thumbnail = models.FileField(blank=True, upload_to='thumbnail/', max_length=512)
    user = models.ForeignKey(User, default=None, null=True, blank=True,
                             on_delete=models.SET_DEFAULT)
    md5 = models.CharField(max_length=32, blank=True)
    sha256 = models.CharField(max_length=64, blank=True)
    sha512 = models.CharField(max_length=128, blank=True)
    collection = models.ForeignKey('Collection', on_delete=models.SET_NULL,
                                   default=None, null=True, blank=True)
    mime_type = models.TextField()

    @property
    def mime_type_category(self):
        """return only the category of the mime_type"""
        return self.mime_type.split('/')[0]

    def update_hashes(self):
        """Update hash properties"""
        with open(self.file.path, 'rb') as _file:
            hashes = generate_hashes(_file)
            for hash_type, hash_value in hashes.items():
                setattr(self, hash_type, hash_value)

    def update_mime(self):
        """Update mime_types from file"""
        self.mime_type = get_mime_type(self.file.name)

    def save(self, *args, **kwargs):
        self.update_hashes()
        self.update_mime()
        return super().save(*args, **kwargs)

    @property
    def sha512_short(self):
        """Get short sha512"""
        return self.sha512[0:16]

    @property
    def get_initial_view(self):
        """Returns the initial view"""
        return ObjectView.objects.filter(obj=self).earliest()

    @property
    def filename(self):
        """Return a filename"""
        return self.sha512

    def __str__(self):
        return self.sha512

class ObjectView(models.Model):
    """Store information about a single view"""
    obj = models.ForeignKey('Object', on_delete=models.CASCADE)
    viewee = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    viewee_ip = models.GenericIPAddressField(blank=True, null=True)
    viewee_dns = models.TextField(blank=True)
    viewee_date = models.DateTimeField(auto_now_add=True)
    viewee_user_agent = models.TextField(blank=True)

    _ua_inst = None

    @property
    def user_agent(self):
        """Return user_agent instance"""
        if not self._ua_inst:
            self._ua_inst = parse(self.viewee_user_agent)
        return self._ua_inst

class Collection(models.Model):
    """Collection to group Objects together"""

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:

        unique_together = (('name', 'owner', ), )
