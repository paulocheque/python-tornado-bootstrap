# coding: utf-8
import sys
sys.path.append('.')

import logging
logging.getLogger().setLevel(logging.INFO)

from fabric.api import task

import connect_mongo
from apps.accounts.models import User
from apps.app.tasks import *


@task
def task1():
    a_task()

@task
def report():
    print('%s users' % User.objects.count())
