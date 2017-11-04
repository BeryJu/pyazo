"""
Supervisr Core Fieldtype filter
"""

from django import template

register = template.Library()

@register.filter('fieldtype')
def fieldtype(field):
    """
    Return classname
    """
    return field.__class__.__name__
