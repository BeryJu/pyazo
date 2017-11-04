"""
Supervisr Core navbar Templatetag
"""

from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def is_active_app(context, *args):
    """
    Return True if current link is from app
    """
    req = context['request']
    if not req.resolver_match:
        return ''
    for app in args:
        if app in req.resolver_match.app_names:
            return 'active'
    return ''
