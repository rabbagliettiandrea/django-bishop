# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from django.core.urlresolvers import reverse
from django.db.models import Model, DateTimeField
from django.utils.html import escape

from bishop.datetime_utils import get_utc_now


class TimedatedModel(Model):
    timestamp_created = DateTimeField(auto_now_add=True, null=True, db_index=True, editable=False)
    timestamp_modified = DateTimeField(auto_now=True, null=True, db_index=True, editable=False)

    class Meta:
        abstract = True


class LinkableFieldModel(Model):
    def get_change_url(self):
        try:
            return reverse(
                "admin:%s_%s_change" % (self._meta.app_label, self._meta.object_name.lower()), args=(self.pk,))
        except Exception as e:
            return unicode(e)

    def get_change_href(self):
        return '<strong><a href="%s">%s</a></strong>' % (self.get_change_url(), escape(self))
    get_change_href.allow_tags = True
    get_change_href.short_description = 'Link'

    class Meta:
        abstract = True
