# coding: utf-8
from datetime import datetime, timedelta

from mongoengine import *

import connect_redis


def split_by_commas(text):
    if isinstance(text, (str, unicode)):
        text = text.split(',')
        text = map(lambda x: x.strip(), text)
    return text


class MyDoc(Document):
    a = EmailField(required=True)
    b = StringField()
    c = StringField()
    date_created = DateTimeField(default=datetime.utcnow)

    def async_task(self):
        queue = connect_redis.default_queue()
        queue.enqueue_call(func='apps.app.tasks.a_task', args=(None,))
