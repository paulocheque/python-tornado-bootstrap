# coding: utf-8
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
import itertools
import logging
import os
import re
from StringIO import StringIO
import urllib

# import qrcode

from apps.utils.serializer import *
from apps.utils.common import *
from apps.utils.security import *
from apps.utils.qr_code import *
from apps.utils.tasks import *
from apps.utils.models import *
from apps.accounts.models import User

from mongoengine import *

import connect_redis


SYSTEM_NAME = os.getenv('SYSTEM_NAME')
SYSTEM_EMAIL = os.getenv('SYSTEM_EMAIL')
SYSTEM_URL = os.getenv('SYSTEM_URL')
DATE_FORMAT = os.getenv('DATE_FORMAT')
TIME_FORMAT = os.getenv('TIME_FORMAT')
DATETIME_FORMAT = os.getenv('DATETIME_FORMAT')


class MyDoc(Document):
    email = EmailField(required=True)
    name = StringField()
    tags = ListField(StringField(max_length=20))

    address = EmbeddedDocumentField(Address)
    phone = EmbeddedDocumentField(Phone)
    credit_card = EmbeddedDocumentField(CreditCard)
    addresses = ListField(EmbeddedDocumentField(Address), required=False)
    phones = ListField(EmbeddedDocumentField(Phone), required=False)
    credit_cards = ListField(EmbeddedDocumentField(CreditCard), required=False)

    # Internal
    slug = StringField()
    qr_code = ImageField(size=(256,256,False))
    date_created = DateTimeField(default=datetime.utcnow)
    date_updated = DateTimeField(default=datetime.utcnow)

    def save(self, **kwargs):
        self.tags = taggify(self.tags)
        self.slug = slugify(self.name)
        if not self.qr_code:
            generate_qrcode(self.qr_code, self.url())
        self.date_updated = datetime.now()
        return super(MyDoc, self).save(**kwargs)

    def url(self):
        return '{system_url}/{slug}'.format(system_url=SYSTEM_URL, slug=self.slug)

    def qrcode_url(self):
        return '{system_url}/{slug}/qrcode'.format(system_url=SYSTEM_URL, slug=self.slug)

    def async_task(self):
        queue = connect_redis.default_queue()
        queue.enqueue_call(func='apps.app.tasks.a_task', args=(None,))
