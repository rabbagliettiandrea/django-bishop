# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
import base64
from Crypto.Cipher import AES
from django.conf import settings

PADDING = '0'
cypher = AES.new(settings.SECRET_KEY[:16])


pad = lambda s: s + PADDING * (AES.block_size - len(s) % AES.block_size)


def encrypt(msg):
    return base64.b16encode(cypher.encrypt(pad(msg))).lower()


def decrypt(msg):
    return cypher.decrypt(base64.b16decode(bytes(msg.upper()))).strip(PADDING)