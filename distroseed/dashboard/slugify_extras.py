from django import template

register = template.Library()

@register.filter
def underscore(value):
    return value.replace(' ', '_')

