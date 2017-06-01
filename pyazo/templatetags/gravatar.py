"""
Supervisr Core Gravatar Templatetag
"""
from hashlib import md5
from urllib.parse import urlencode

from django import template
from django.utils.html import escape

register = template.Library()

@register.simple_tag
def gravatar(email, size=None, rating=None):
    """
    Generates a Gravatar URL for the given email address.

    Syntax::

        {% gravatar <email> [size] [rating] %}

    Example::

        {% gravatar someone@example.com 48 pg %}
    """
    gravatar_url = "%savatar/%s" % ('https://secure.gravatar.com/',
                                    md5(email.encode('utf-8')).hexdigest())

    parameters = [p for p in (
        ('s', size or '158'),
        ('r', rating or 'g'),
    ) if p[1]]

    if parameters:
        gravatar_url += '?' + urlencode(parameters, doseq=True)

    return escape(gravatar_url)
