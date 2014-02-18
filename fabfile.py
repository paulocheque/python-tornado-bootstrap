import sys
sys.path.append('.')

from fabric.api import task

@task
def task1():
    print('task 1')
