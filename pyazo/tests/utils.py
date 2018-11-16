"""testing utilities"""
from django.contrib.auth.models import User


def test_auth():
    """Create a test user and return credentials to use with client.login"""
    creds = {
        'username': 'test',
        'password': 'test',
    }
    User.objects.create_user(**creds)
    return creds
