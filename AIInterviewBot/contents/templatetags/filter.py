from django import template

register = template.Library()

@register.filter
def length(value):
    return len(value)