"""pyazo Core Account Views"""
from logging import getLogger

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import ugettext as _

from pyazo.decorators import anonymous_required
from pyazo.forms.account import LoginForm
from pyazo.utils.config import CONFIG

LOGGER = getLogger(__name__)


@anonymous_required
def login(request):
    """View to handle Browser Logins Requests"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'))

            if user is not None:
                django_login(request, user)
                # Set updated password in user profile for PAM

                if not form.cleaned_data.get('remember'):
                    request.session.set_expiry(0) # Expires when browser is closed
                messages.success(request, _("Successfully logged in!"))
                LOGGER.info("Successfully logged in %s", form.cleaned_data.get('username'))
                # Check if there is a next GET parameter and redirect to that
                if 'next' in request.GET:
                    return redirect(request.GET.get('next'))
                # Otherwise just index
                return redirect(reverse('index'))
            # Check if the user's account is pending
            # and inform that, they need to check their usernames
            # users = User.objects.filter(username=form.cleaned_data.get('username'))
            messages.error(request, _("Invalid Login"))
            LOGGER.info("Failed to log in %s", form.cleaned_data.get('username'))
            return redirect(reverse('accounts-login'))
        LOGGER.info("Form invalid")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {
        'form': form,
        'title': _("SSO - Login"),
        'primary_action': _("Login"),
        'external_only': CONFIG.get('external_auth_only'),
        })

def logout(request):
    """Logout"""
    django_logout(request)
    messages.success(request, _("Successfully logged out!"))
    return redirect(reverse('index'))
