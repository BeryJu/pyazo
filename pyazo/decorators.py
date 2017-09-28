"""
pyazo view decorators
"""

import base64
import time

from django.apps import apps
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode


def anonymous_required(view_function):
    """
    Decorator to only allow a view for anonymous users
    """
    def wrap(*args, **kwargs):
        """
        Check if request's user is authenticated and route back to index
        """
        req = args[0] if args else None
        if req and req.user is not None and req.user.is_authenticated():
            return redirect(reverse('common-index'))
        return view_function(*args, **kwargs)

    wrap.__doc__ = view_function.__doc__
    wrap.__name__ = view_function.__name__
    return wrap
