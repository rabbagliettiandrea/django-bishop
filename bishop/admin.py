# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.contrib.admin.models import DELETION, LogEntry
from django.core.urlresolvers import reverse
from django.utils.html import escape


class LogEntryAdmin(ModelAdmin):

    class LogEntry_ActionFilter(SimpleListFilter):
        title = "Action"
        parameter_name = 'action'

        def lookups(self, request, model_admin):
            return LogEntryAdmin.ACTION_FLAGS.items()

        def queryset(self, request, queryset):
            if self.value() is not None:
                return queryset.filter(action_flag=self.value())
            return queryset

    ACTION_FLAGS = {1: 'ADDITION', 2: 'CHANGE', 3: 'DELETION'}
    date_hierarchy = 'action_time'
    readonly_fields = [x.name for x in LogEntry._meta.local_fields]
    list_filter = (LogEntry_ActionFilter,)
    search_fields = ('object_repr', 'change_message')
    list_display = ('action_time', 'user', 'content_type', 'object_link', 'action_verbose', 'change_message',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def action_verbose(self, obj):
        return LogEntryAdmin.ACTION_FLAGS[obj.action_flag]

    def object_link(self, obj):
        try:
            if obj.action_flag == DELETION:
                link = escape(obj.object_repr)
            else:
                ct = obj.content_type
                link = u'<a href="%s">%s</a>' % (
                    reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                    escape(obj.object_repr),
                )
        except:
            return None
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')
