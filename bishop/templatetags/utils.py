# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from decimal import Decimal
from django import template
from math import ceil, floor
from django.core.urlresolvers import reverse


register = template.Library()


@register.filter
def as_range(value):
    try:
        value = int(ceil(value))
        return xrange(value)
    except:
        return None


@register.filter
def add_float(x, y):
    return x + y


@register.assignment_tag
def split_number(value):
    try:
        value = Decimal(value)
    except:
        return value
    value_floor = Decimal(floor(value))
    d = {
        'floor': value_floor,
        'mantissa': value - value_floor
    }
    return d


@register.simple_tag(takes_context=True)
def absolute_url(context, viewname):
    request = context.get('request')
    if not request:
        raise RuntimeError('request is None')
    return request.build_absolute_uri(reverse(viewname))