# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.conf import settings
from django.utils import timezone
import pytz


def make_aware_tz(dtime):
    return timezone.make_aware(dtime, timezone=pytz.timezone(settings.TIME_ZONE))


def get_utc_today():
    return timezone.now().date()


def get_local_today():
    return timezone.localtime(timezone.now()).date()


def get_utc_now():
    return timezone.now()


def get_local_now():
    return timezone.localtime(timezone.now())


def get_current_year():
    return get_local_now().year