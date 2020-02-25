# Generated by Django 2.1.2 on 2018-10-11 19:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pyazo_core", "0010_auto_20181011_1854"),
    ]

    operations = [
        migrations.AlterField(
            model_name="upload",
            name="collection",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="pyazo_core.Collection",
            ),
        ),
    ]