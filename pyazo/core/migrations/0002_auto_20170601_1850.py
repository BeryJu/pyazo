# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 16:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pyazo_core", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(old_name="UplodaView", new_name="UploadView",),
    ]