"""pyazo view decorators"""

from functools import wraps

from django.shortcuts import redirect
from django.urls import reverse


def anonymous_required(view_function):
    """Decorator to only allow a view for anonymous users"""

    @wraps(view_function)
    def wrap(*args, **kwargs):
        """Check if request's user is authenticated and route back to index"""
        requests = args[0] if args else None
        if requests and requests.user is not None and requests.user.is_authenticated:
            return redirect(reverse("index"))
        return view_function(*args, **kwargs)

    return wrap
