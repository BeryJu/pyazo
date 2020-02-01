"""Pyazo generate_secret_key management command"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Generate Django secret key"""

    def handle(self, *args, **options):
        """Generate Django secret key"""
        import random

        self.stdout.write(
            "".join(
                [
                    random.SystemRandom().choice(
                        "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
                    )
                    for i in range(50)
                ]
            )
        )
