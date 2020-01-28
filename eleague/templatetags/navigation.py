from django import template
from django.shortcuts import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def is_nav_active(context, reverse_name):
    return 'is-active' if reverse(reverse_name) in context.request.path else ''
