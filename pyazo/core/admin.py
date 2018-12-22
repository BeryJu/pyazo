"""pyazo admin"""
from django.contrib import admin

from pyazo.core.models import Collection, Object, ObjectView

admin.site.register(Object)
admin.site.register(ObjectView)
admin.site.register(Collection)
