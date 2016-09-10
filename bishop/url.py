# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from urlparse import urljoin
from django.conf import settings
from django.utils.encoding import force_text


def build_full_url(url):
    return urljoin(settings.SITE_URL, force_text(url))