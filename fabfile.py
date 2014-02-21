import sys
sys.path.append('.')

import logging
logging.getLogger().setLevel(logging.INFO)

from fabric.api import task

from apps.app.tasks import *


@task
def task1():
    a_task()
