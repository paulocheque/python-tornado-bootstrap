# coding: utf-8
from datetime import datetime, timedelta

from mongoengine import *

from apps.utils.common import *

import connect_redis


class MyDoc(Document):
    a = EmailField(required=True)
    b = StringField()
    c = StringField()
    tags = ListField(StringField(max_length=20))
    date_created = DateTimeField(default=datetime.utcnow)

    def save(self, **kwargs):
        self.tags = smart_split(self.tags)
        return super(MyDoc, self).save(**kwargs)

    def async_task(self):
        queue = connect_redis.default_queue()
        queue.enqueue_call(func='apps.app.tasks.a_task', args=(None,))
