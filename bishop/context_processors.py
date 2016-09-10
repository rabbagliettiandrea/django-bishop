# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.conf import settings
from django.utils import timezone


def get__settings(request):
    return {'settings': lambda: settings}


def get__datetime_now(request):
    return {'datetime_now': lambda: timezone.localtime(timezone.now())}


def get__client_is_logged(request):
    return {'client_is_logged': lambda: request.user.is_authenticated() and not request.user.is_staff}


def get__base_url(request):
    return {'base_url': lambda: '%s://%s' % (request.scheme, request.get_host())}