"""
pyazo Core Account Forms
"""

import logging

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils.translation import ugettext as _

from pyazo.forms.core import InlineForm, check_password

LOGGER = logging.getLogger(__name__)

class LoginForm(InlineForm):
    """
    Form to handle logins
    """
    order = ['username', 'password', 'remember']
    username = forms.CharField(label=_('Mail'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))
    remember = forms.BooleanField(required=False, label=_('Remember'))
