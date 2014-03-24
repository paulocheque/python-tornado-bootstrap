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
from apps.utils.tasks import *
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
    slug = StringField()
    tags = ListField(StringField(max_length=20))
    date_created = DateTimeField(default=datetime.utcnow)

    def save(self, **kwargs):
        self.tags = taggify(self.tags)
        self.slug = slugify(self.name)
        return super(MyDoc, self).save(**kwargs)

    def async_task(self):
        queue = connect_redis.default_queue()
        queue.enqueue_call(func='apps.app.tasks.a_task', args=(None,))
