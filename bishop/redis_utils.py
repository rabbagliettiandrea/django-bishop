# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.conf import settings
import redis
import cPickle as pickle


class _PicklingRedis(redis.Redis):
    def get(self, name):
        pickled_value = super(_PicklingRedis, self).get(name)
        return pickled_value and pickle.loads(pickled_value)

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        return super(_PicklingRedis, self).set(name, pickle.dumps(value), ex, px, nx, xx)


def get_db(alias):
    return _PicklingRedis().from_url('redis://%s' % '/'.join(settings.REDIS_SERVERS[alias]))


def reset_stats():
    client = _PicklingRedis()
    client.execute_command('CONFIG RESETSTAT')