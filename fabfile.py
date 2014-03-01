# coding: utf-8
import sys
sys.path.append('.')

import logging
logging.getLogger().setLevel(logging.INFO)

from fabric.api import task

import connect_mongo
from apps.accounts.models import User
from apps.app.tasks import *


# https://gist.github.com/paulocheque/5906909
def colorize(message, color='blue'):
    color_codes = dict(black=30, red=31, green=32, yellow=33, blue=34, magenta=35, cyan=36, white=37)
    code = color_codes.get(color, 34)
    msg = '\033[%(code)sm%(message)s\033[0m' % {'code':code, 'message':message}
    # print(msg)
    return msg


@task
def task1():
    a_task()

@task
def report():
    print('%s users' % User.objects.count())
    print('-' * 50)