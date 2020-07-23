"""testing utilities"""
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command


def test_auth(superuser=True):
    """Create a test user and return credentials to use with client.login"""
    credentials = {
        "username": "test",
        "password": "test",
        "email": "test@test.test",
    }
    if superuser:
        credentials["username"] = "superuser"
        get_user_model().objects.create_superuser(**credentials)
    else:
        credentials["username"] = "user"
        get_user_model().objects.create_user(**credentials)
    return credentials


def call_command_ret(*args, **kwargs):
    """This is a wrapper for django's call_command, but it returns the stdout output"""
    with StringIO() as output:
        call_command(*args, stdout=output, stderr=output, **kwargs)
        return output.getvalue()
