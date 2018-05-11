"""pyazo view decorators"""

from django.shortcuts import redirect
from django.urls import reverse


def anonymous_required(view_function):
    """Decorator to only allow a view for anonymous users"""
    def wrap(*args, **kwargs):
        """Check if request's user is authenticated and route back to index"""
        req = args[0] if args else None
        if req and req.user is not None and req.user.is_authenticated:
            return redirect(reverse('common-index'))
        return view_function(*args, **kwargs)

    wrap.__doc__ = view_function.__doc__
    wrap.__name__ = view_function.__name__
    return wrap
