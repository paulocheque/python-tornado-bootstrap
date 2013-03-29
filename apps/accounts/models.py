# coding: utf-8
from datetime import datetime

from mongoengine import *


class User(Document):
    email = StringField(required=True)
    password = StringField(required=True)
    registered_on = DateTimeField(required=True, default=datetime.utcnow())
