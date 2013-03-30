# coding: utf-8
import redis
import os
from mongoengine import *

try:
    ENVIRONMENT = open('environment', 'r').read().strip()
except IOError:
    ENVIRONMENT = 'heroku'

if ENVIRONMENT == 'heroku':
    # Redis
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    R = redis.from_url(redis_url)

    # $ heroku config:add MONGO_UN=...
    # $ heroku config:add MONGO_PW=...
    # $ heroku config:add MONGO_HOST=...
    # $ heroku config:add MONGO_PORT=...
    # $ heroku config:add MONGO_db=...
    # mongo_un = os.environ['MONGO_UN']
    # mongo_pw = os.environ['MONGO_PW']
    # mongo_db = os.environ['MONGO_DB']
    # mongo_host = os.environ['MONGO_HOST']
    # mongo_port = int(os.environ['MONGO_PORT'])

    mongo_url = os.environ['MONGOHQ_URL']
    connect('default', host=mongo_url)
else:
    # Local
    R = redis.StrictRedis()
    connect('default')
