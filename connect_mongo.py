# coding: utf-8
import os
from mongoengine import *


mongo_url = os.environ.get('MONGOHQ_URL', None)
if mongo_url:
    print('Connecting to PRODUCTION MongoDB')
    connect('default', host=mongo_url)
else:
    print('Connecting to DEV MongoDB')
    connect('default')
