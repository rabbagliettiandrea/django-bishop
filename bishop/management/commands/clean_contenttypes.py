# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
import traceback

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Clean django ContentType model'

    def handle(self, limit=None, *args, **options):
        try:
            for c in ContentType.objects.all():
                if not c.model_class():
                    self.stdout.write('Deleting [{}.{}]'.format(c.app_label, c.model))
                    confirm = raw_input("Are you sure? Type 'yes' to continue: ")
                    if confirm == 'yes':
                        c.delete()
        except:
            traceback.print_exc()
        finally:
            self.stdout.write('\nFinished.')
