#!/usr/bin/env bash
import logging
import os

from rq import Worker, Queue, Connection

import connect_mongo
import connect_redis

# logging.getLogger().setLevel(logging.INFO)

def task_timeout_handler(job, exc_type, exc_value, traceback):
    logging.error('Worker error handler')
    logging.error('%s %s %s' % (exc_type, exc_value, traceback))
    # if exc_type == DequeueTimeout or exc_type == JobTimeoutException:
    #     pass # Timeout
    # else:
    #     pass # Unknown


# http://python-rq.org/
# https://github.com/nvie/rq/
# http://python-rq.org/docs/
# http://python-rq.org/docs/results/
# http://python-rq.org/docs/exceptions/
def listen_queue(queues=['default']):
    redis_connection = connect_redis.connect_to_redis()
    with Connection(redis_connection):
        worker = Worker(map(Queue, queues))
        worker.push_exc_handler(task_timeout_handler)
        worker.work()


if __name__ == '__main__':
    listen_queue()
