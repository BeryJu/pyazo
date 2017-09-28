"""
pyazo Core back Templatetag
"""

from urllib.parse import urlparse

from django import template

register = template.Library()


def is_absolute(url):
    """
    Check if domain is absolute to
    prevent user from being redirect somehwere else
    """
    return bool(urlparse(url).netloc)

@register.simple_tag(takes_context=True)
def back(context):
    """
    Return whether a back link is active or not.
    """

    req = context['request']
    if 'back' in req.GET:
        if not is_absolute(req.GET.get('back')):
            return req.GET.get('back')
    if 'HTTP_REFERER' in req.META:
        if not is_absolute(req.META.get('HTTP_REFERER')):
            return req.META.get('HTTP_REFERER')
    return ''
