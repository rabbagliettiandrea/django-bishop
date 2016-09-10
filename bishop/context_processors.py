# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division


def settings(request):
    from django.conf import settings
    return {'settings': lambda: settings}


def datetime_now(request):
    from django.utils import timezone
    return {'datetime_now': lambda: timezone.localtime(timezone.now())}
