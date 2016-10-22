from django import template
register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    return value*arg


@register.filter(name='min2hour')
def min2hour(value):
    return value/60.0;
