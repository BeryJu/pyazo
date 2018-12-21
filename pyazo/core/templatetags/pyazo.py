"""pyazo sidebar collection Templatetag"""

from urllib.parse import urlparse

from django import template

from pyazo.core.models import Collection

register = template.Library()


@register.simple_tag(takes_context=True)
def collections(context):
    """Return User's Collections"""
    request = context['request']
    if request.user.is_authenticated:
        return Collection.objects.filter(owner=request.user)
    return []


@register.filter('fieldtype')
def fieldtype(field):
    """Return classname"""
    return field.__class__.__name__


def is_absolute(url):
    """Check if domain is absolute to
    prevent user from being redirect somewhere else"""
    return bool(urlparse(url).netloc)


@register.simple_tag(takes_context=True)
def back(context):
    """Return whether a back link is active or not."""
    request = context.get('request')
    if 'back' in request.GET:
        if not is_absolute(request.GET.get('back')):
            return request.GET.get('back')
    if 'HTTP_REFERER' in request.META:
        if not is_absolute(request.META.get('HTTP_REFERER')):
            return request.META.get('HTTP_REFERER')
    return ''


@register.simple_tag(takes_context=True)
def is_active(context, *args):
    """Return whether a navbar link is active or not."""
    request = context.get('request')
    if not request.resolver_match:
        return ''
    for url in args:
        short_url = url.split(':')[1] if ':' in url else url
        if request.resolver_match.url_name.startswith(url) or \
                request.resolver_match.url_name.startswith(short_url):
            return 'active'
    return ''


@register.simple_tag(takes_context=True)
def is_active_app(context, *args):
    """Return True if current link is from app"""
    request = context.get('request')
    if not request.resolver_match:
        return ''
    for app in args:
        if app in request.resolver_match.app_names:
            return 'active'
    return ''
