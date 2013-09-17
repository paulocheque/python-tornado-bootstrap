# coding: utf-8
import redis
import os
from mongoengine import *


mongo_url = os.environ.get('MONGOHQ_URL', None)
if mongo_url:
    connect('default', host=mongo_url)
else:
    connect('default')


redis_url = os.environ.get('REDISTOGO_URL', None)
if redis_url:
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    R = redis.from_url(redis_url)
else:
    R = redis.StrictRedis()
    connect('default')
