# coding: utf-8
from datetime import datetime

from mongoengine import *


class SystemSettings(Document):
    memory_cache = None # One query per load/update
    # Internal control
    singleton = StringField(unique=True, choices=('1', '1'), default='1')
    date_updated = DateTimeField(default=datetime.utcnow)
    # custom settings
    max_emails_per_day = IntField(default=200)
    # ex1 = BooleanField()
    # ex2 = StringField(choices=(('A'),('A')), max_length=2)

    @classmethod
    def get(cls):
        if SystemSettings.memory_cache is not None:
            return SystemSettings.memory_cache
        else:
            ss, created = SystemSettings.objects.get_or_create(singleton='1')
            SystemSettings.memory_cache = ss
            return ss

    @classmethod
    def refresh(cls):
        SystemSettings.memory_cache = None
        return SystemSettings.get()

    @classmethod
    def show(cls):
        ss = SystemSettings.get()
        for k, v in vars(ss)['_data'].items():
            if k != 'singleton' and k != 'id':
                print('%s: %s' % (k, v))

    def __str__(self):
        return '[%s] ' % self.date_updated

    def save(self, **kwargs):
        date_updated = datetime.utcnow()
        super(SystemSettings, self).save(**kwargs)
        return SystemSettings.refresh()
