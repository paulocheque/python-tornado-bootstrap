# coding: utf-8
import sys
sys.path.append('.')

import logging
logging.getLogger().setLevel(logging.INFO)

from fabric.api import task

from apps.app.tasks import *


@task
def task1():
    a_task()

@task
def report():
    from apps.accounts.models import User
    print('%s users' % User.objects.count())
