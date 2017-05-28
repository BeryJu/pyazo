from django.db import models
from django.contrib.auth.models import User

UPLOAD_TYPES = (
    (0, 'Picture'),
)

class Upload(models.Model):
    filename = models.TextField(max_length=512)
    type = models.IntegerField(choices=UPLOAD_TYPES)
    uploader_ip = models.GenericIPAddressField()
    uploaded_by = models.ForeignKey(User, blank=True, null=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
