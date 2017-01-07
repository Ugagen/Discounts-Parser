from django.template import Library

register = Library()


@register.filter
def times(value):
    return range(value)


@register.filter
def star(value, arg):
    return range(5-value-arg)


@register.filter
def toList(value):
    return value.split(' , ')
