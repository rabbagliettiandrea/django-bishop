# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
import codecs
import json
import os
from unicodecsv import DictWriter, DictReader
from django.conf import settings


def write_file_json(data, filepath):
    with codecs.open(filepath, 'w', encoding=settings.DEFAULT_CHARSET, errors='ignore') as fd:
        json.dump(data, fd, indent=True, encoding=settings.DEFAULT_CHARSET, ensure_ascii=False)


def read_file_json(filepath, lower=False):
    if not os.path.isfile(filepath):
        return None
    with codecs.open(filepath, 'r', encoding=settings.DEFAULT_CHARSET, errors='ignore') as fd:
        file_content = fd.read()
    if lower:
        file_content = file_content.lower()
    data = json.loads(file_content, encoding=settings.DEFAULT_CHARSET)
    return data


def write_file_csv(data, fieldnames, filepath):
    with codecs.open(filepath, 'w', encoding=settings.DEFAULT_CHARSET, errors='ignore') as fd:
        if data:
            writer = DictWriter(fd, fieldnames=fieldnames, errors='ignore')
            writer.writeheader()
            for d in data:
                try:
                    writer.writerow(d)
                except UnicodeDecodeError:
                    pass


def read_file_csv(filepath):
    if not os.path.isfile(filepath):
        return None
    with codecs.open(filepath, 'r', encoding=settings.DEFAULT_CHARSET, errors='ignore') as fd:
        return [row for row in DictReader(fd, errors='ignore')]
