import sys
sys.path.append('.')

import logging
logging.getLogger().setLevel(logging.INFO)

from fabric.api import task

@task
def task1():
    print('task 1')
