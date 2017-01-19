from django import template
from django.http import QueryDict

register = template.Library()


@register.filter(name='split')
def split(value, args):
    qs = QueryDict(args)
    if 'deli' in qs and 'site' in qs:
        return value.split(qs['deli'])[int(qs['site'])]
    else:
        return value
