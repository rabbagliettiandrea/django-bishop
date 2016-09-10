# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
import json
from django.http import HttpResponse, JsonResponse
from django.utils.encoding import force_text


def make_json_response(d=None, redirect_url=None):
    if not d:
        d = {}
    if redirect_url:
        d['redirect_url'] = force_text(redirect_url)
    return JsonResponse(d)


def make_json_response_form(forms, additional_data=None, redirect_url=None):
    d = {
        'fields': [],
        'errors': {}
    }

    if additional_data:
        d.update(additional_data)

    for form in forms:
        prefix = form.prefix and form.prefix + '-' or ''

        form_fields = []
        for v in form.fields:
            form_fields.append(prefix + v)

        form_errors = {}
        for k, v in form.errors.iteritems():
            if k != '__all__':
                form_errors[prefix + k] = v

        d['fields'].extend(form_fields)
        d['errors'].update(form_errors)

        if '__all__' in form.errors:
            errors = d['errors'].setdefault('__all__', [])
            errors.extend(form.errors['__all__'])

    return make_json_response(d, redirect_url=redirect_url)