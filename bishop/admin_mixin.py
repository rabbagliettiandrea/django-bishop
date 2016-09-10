# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.contrib.admin import site
from django.contrib.admin.options import csrf_protect_m
from django.contrib.admin.utils import unquote
from django.contrib.admin.widgets import ForeignKeyRawIdWidget, ManyToManyRawIdWidget
from django.core.urlresolvers import reverse
from django.contrib.admin.widgets import AdminDateWidget
from django.db.models import DateField
from django.utils.html import escape
from django.utils.safestring import mark_safe


class DistinctQuerysetMixin(object):
    def get_queryset(self, request):
        return super(DistinctQuerysetMixin, self).get_queryset(request).distinct()


class WarningableMixin(object):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['warning_message'] = self.warning_message
        return super(WarningableMixin, self).change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context
        )


class DatePlaceholderMixin(object):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, DateField):
            kwargs['widget'] = AdminDateWidget(attrs={'placeholder': 'gg/mm/aaaa',
                                                      'style': 'width: 75px;'})
            kwargs.pop('request')
            return db_field.formfield(**kwargs)
        return super(DatePlaceholderMixin, self).formfield_for_dbfield(db_field, **kwargs)


class PostSaveMixin(object):
    def response_add(self, request, obj, post_url_continue=None):
        response = super(PostSaveMixin, self).response_add(request, obj, post_url_continue=None)
        self.post_save(request, obj)
        return response

    def response_change(self, request, obj):
        response = super(PostSaveMixin, self).response_change(request, obj)
        self.post_save(request, obj)
        return response

    def changelist_view(self, request, extra_context=None):
        to_change = []
        if request.method == "POST" and '_save' in request.POST:
            FormSet = self.get_changelist_formset(request)
            formset = FormSet(request.POST, request.FILES)
            if formset.is_valid():
                changecount = 0
                for form in formset.forms:
                    if form.has_changed():
                        obj = self.save_form(request, form, change=True)
                        to_change.append(obj)
        response = super(PostSaveMixin, self).changelist_view(request, extra_context=extra_context)
        for obj in to_change:
            self.post_save(request, obj)
        return response


class PostChangelistSaveMixin(object):
    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        response = super(PostChangelistSaveMixin, self).changelist_view(request, extra_context)
        if request.method == 'POST':
            self.post_changelist_save(request, extra_context)
        return response


class PostCreateMixin(object):
    def response_add(self, request, obj, post_url_continue=None):
        response = super(PostCreateMixin, self).response_add(request, obj, post_url_continue=None)
        self.post_create(request, obj)
        return response


class PostEditMixin(object):
    def response_change(self, request, obj):
        response = super(PostEditMixin, self).response_change(request, obj)
        self.post_edit(request, obj)
        return response


class NotAddableMixin(object):
    def has_add_permission(self, request, obj=None):
        return False


class NotDeletableMixin(object):
    def get_actions(self, request):
        actions = super(NotDeletableMixin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class ClickableRawFieldsMixin(object):
    class VerboseManyToManyRawIdWidget(ManyToManyRawIdWidget):
        def label_for_value(self, value):
            values = value.split(',')
            str_values = []
            key = self.rel.get_related_field().name
            for v in values:
                try:
                    obj = self.rel.to._default_manager.using(self.db).get(**{key: v})
                    x = unicode(obj)
                    change_url = reverse(
                        "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.object_name.lower()),
                        args=(obj.pk,)
                    )
                    str_values += ['<strong><a href="%s">%s</a></strong>' % (change_url, escape(x))]
                except self.rel.to.DoesNotExist:
                    str_values += ['???']
            return ', '.join(str_values)

    class VerboseForeignKeyRawIdWidget(ForeignKeyRawIdWidget):
        def render(self, name, value, attrs=None):
            """ For updating raw_id_fields realtime with verbose url """
            original_output = \
                super(ClickableRawFieldsMixin.VerboseForeignKeyRawIdWidget, self).render(name, value, attrs)
            return mark_safe('%s<span id=id_%s_display></span>' % (original_output, name))

        def label_for_value(self, value):
            key = self.rel.get_related_field().name
            try:
                obj = self.rel.to._default_manager.using(self.db).get(**{key: value})
                change_url = reverse(
                    "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.object_name.lower()),
                    args=(obj.pk,)
                )
                return '&nbsp;<strong><a href="%s">%s</a></strong>' % (change_url, escape(obj))
            except (ValueError, self.rel.to.DoesNotExist):
                return '???'

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.raw_id_fields:
            kwargs.pop("request", None)
            t = db_field.rel.__class__.__name__
            if t == "ManyToOneRel" or t == "OneToOneRel":
                kwargs['widget'] = ClickableRawFieldsMixin.VerboseForeignKeyRawIdWidget(
                    db_field.rel, site)
            elif t == "ManyToManyRel":
                kwargs['widget'] = ClickableRawFieldsMixin.VerboseManyToManyRawIdWidget(
                    db_field.rel, site)
            return db_field.formfield(**kwargs)
        return super(ClickableRawFieldsMixin, self).formfield_for_dbfield(db_field, **kwargs)


class DifferentFieldsMixin(object):
    def get_fieldsets(self, request, obj=None):
        if obj:
            return self.modify_fieldsets
        return self.create_fieldsets

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.modify_readonly_fields
        return self.create_readonly_fields


class DifferentInlinesMixin(object):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = self.modify_inlines
        return super(DifferentInlinesMixin, self).change_view(request, object_id)

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = self.create_inlines
        return super(DifferentInlinesMixin, self).add_view(request)


class LinkOnSiteMixin(object):
    def link_on_site(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (obj.get_absolute_url(), obj.get_absolute_url()))
