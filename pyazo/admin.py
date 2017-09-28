"""
pyazo admin
"""
from django.contrib import admin

from pyazo.models import Upload, UploadView

admin.site.register(Upload)
admin.site.register(UploadView)
