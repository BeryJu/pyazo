"""
pyazo Core Account Views
"""

import logging

from allaccess.models import Provider
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import ugettext as _

from pyazo.decorators import anonymous_required
from pyazo.forms.account import LoginForm

LOGGER = logging.getLogger(__name__)


@anonymous_required
def login(req):
    """
    View to handle Browser Logins Requests
    """
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'))

            if user is not None:
                django_login(req, user)
                # Set updated password in user profile for PAM

                if not form.cleaned_data.get('remember'):
                    req.session.set_expiry(0) # Expires when browser is closed
                messages.success(req, _("Successfully logged in!"))
                LOGGER.info("Successfully logged in %s", form.cleaned_data.get('username'))
                # Check if there is a next GET parameter and redirect to that
                if 'next' in req.GET:
                    return redirect(req.GET.get('next'))
                # Otherwise just index
                return redirect(reverse('core-index'))
            else:
                # Check if the user's account is pending
                # and inform that, they need to check their usernames
                # users = User.objects.filter(username=form.cleaned_data.get('username'))
                messages.error(req, _("Invalid Login"))
                LOGGER.info("Failed to log in %s", form.cleaned_data.get('username'))
                return redirect(reverse('core-accounts_login'))
        else:
            print("Form invalid")
    else:
        form = LoginForm()
    return render(req, 'account/login.html', {
        'form': form,
        'title': _("SSO - Login"),
        'primary_action': _("Login"),
        'oauth_providers': Provider.objects.all(),
        'external_only': settings.EXTERNAL_AUTH_ONLY,
        })
