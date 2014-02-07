# coding: utf-8
import redis
import os


class RedisConnection(object):
    connection = None


def connect_to_redis():
    if RedisConnection.connection:
        return RedisConnection.connection
    else:
        redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
        if redis_url != 'redis://localhost:6379':
            print('Connecting to PRODUCTION redis')
        else:
            # RedisConnection.connection = redis.StrictRedis()
            print('Connecting to DEV redis')
        RedisConnection.connection = redis.from_url(redis_url)
        return RedisConnection.connection
