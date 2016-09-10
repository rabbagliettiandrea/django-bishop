# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from StringIO import StringIO
import csv
from importlib import import_module
import os
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.conf import settings


def get_csv_response(request, rows, filename_prefix, delimiter=b';'):
    csv_io = StringIO()
    writer = csv.writer(csv_io, delimiter=delimiter)
    for row in rows:
        writer.writerow([unicode(item).encode(settings.CSV_ENCODING, errors='ignore') for item in row])
    response = HttpResponse(content=csv_io.getvalue(), content_type='text/csv')
    csv_io.close()
    timestamp_creazione__gte = request.GET.get('timestamp_creazione__gte')
    timestamp_creazione__lte = request.GET.get('timestamp_creazione__lte')
    filename = "%s%s%s.csv" % (
        filename_prefix,
        '-da_' + timestamp_creazione__gte if timestamp_creazione__gte else '',
        '-a_' + timestamp_creazione__lte if timestamp_creazione__lte else ''
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def get_client_ip(request_meta):
    x_forwarded_for = request_meta.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request_meta.get('REMOTE_ADDR')
    return ip


def n_inline_in_form(data, name):
    n = int(data[name + '_set-TOTAL_FORMS'])
    if data.get(name + '_set-0-DELETE') == 'on':
        n -= 1
    return n


def get_sessionstore_class():
    return import_module(settings.SESSION_ENGINE).SessionStore


def get_user_from_session_id(session_id):
    SessionStore = get_sessionstore_class()
    try:
        session_data = SessionStore(session_key=session_id)
        return get_user_model().objects.get(id=session_data.get('_auth_user_id'))
    except ObjectDoesNotExist:
        from django.contrib.auth.models import AnonymousUser
        return AnonymousUser()


def price_to_int(price):
    return int(round(price * 100, 0))


def import_object(object_path):
    module_path, object_name = object_path.rsplit('.', 1)
    return getattr(import_module(module_path), object_name)


def chunks(sequence, n):
    """Yield successive n-sized chunks from l"""
    for i in xrange(0, len(sequence), n):
        yield sequence[i:i+n]