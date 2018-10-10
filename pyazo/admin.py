"""pyazo admin"""
from django.contrib import admin

from pyazo.models import Collection, Upload, UploadView

admin.site.register(Upload)
admin.site.register(UploadView)
admin.site.register(Collection)
