"""
pyazo Core Account Forms
"""

import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

LOGGER = logging.getLogger(__name__)

class LoginForm(forms.Form):
    """
    Form to handle logins
    """
    order = ['username', 'password', 'remember']
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))
    remember = forms.BooleanField(required=False, label=_('Remember'))
