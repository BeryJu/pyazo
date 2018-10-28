"""Pyazo nexus_upload management command"""
import os
from glob import glob

import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Upload debian package to nexus repository"""

    def handle(self, *args, **options):
        """Upload debian package to nexus repository"""
        nexus_url = os.environ.get('NEXUS_URL')
        nexus_user = os.environ.get('NEXUS_USER')
        nexus_pass = os.environ.get('NEXUS_PASS')
        print(requests.post('https://%s/repository/apt/' % nexus_url,
                            data=open(glob('../pyazo-python3.5_*')[0], mode='rb'),
                            auth=(nexus_user, nexus_pass)))
