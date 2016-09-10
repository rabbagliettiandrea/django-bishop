# -*- coding: utf-8 -*-


from __future__ import unicode_literals, division, absolute_import
from django import template
import json


register = template.Library()


@register.filter
def prettify(data):
    return json.dumps(data, indent=3)