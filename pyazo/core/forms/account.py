"""pyazo Core Account Forms"""

from django import forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    """Form to handle logins"""

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, label=_("Password"))
    remember = forms.BooleanField(required=False, label=_("Remember"))
