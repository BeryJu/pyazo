"""pyazo sidebar collection Templatetag"""

from django import template

from pyazo.models import Collection

register = template.Library()


@register.simple_tag(takes_context=True)
def collections(context):
    """Return User's Collections"""
    request = context['request']
    return Collection.objects.filter(owner=request.user)
