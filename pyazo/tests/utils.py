"""testing utilities"""
from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command


def test_auth():
    """Create a test user and return credentials to use with client.login"""
    creds = {
        'username': 'test',
        'password': 'test',
        'email': 'test@test.test',
    }
    User.objects.create_superuser(**creds)
    return creds


def call_command_ret(*args, **kwargs):
    """This is a wrapper for django's call_command, but it returns the stdout output"""
    with StringIO() as output:
        call_command(*args, stdout=output, stderr=output, **kwargs)
        return output.getvalue()
