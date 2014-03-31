# coding: utf-8
import logging
import os
import re
from StringIO import StringIO
import sys

import requests
import sendgrid

from py_social.facebook_services import *
from py_social.twitter_services import tweet

import settings # import to set env variables
import connect_mongo # import to connect to the database
import connect_redis # import to connect to redis
from .common import str2bool


def send_email(to, subject, body):
    test_mode = str2bool(os.getenv('TEST_MODE', False))
    if test_mode:
        logging.info('Sending e-mail {subject} to {to}'.format(subject=subject, to=to))
    else:
        try:
            sg = sendgrid.SendGridClient(os.getenv('SENDGRID_USERNAME'), os.getenv('SENDGRID_PASSWORD'))
            message = sendgrid.Mail(to=to,
                                    subject='[%s] %s' % (os.getenv('SYSTEM_NAME'), subject),
                                    html=body,
                                    text=body,
                                    from_email=os.getenv('SYSTEM_EMAIL'))
            sg.send(message)
        except Exception as e:
            logging.error(str(e))
            logging.exception(e)


def send_admin_email(subject, body):
    send_email(os.getenv('ADMIN_EMAIL'), subject, body)


def async_send_email(to, subject, body):
    async = str2bool(os.getenv('ASYNC_TASKS', True))
    if async:
        queue = connect_redis.default_queue()
        queue.enqueue(send_email, to, subject, body)
        logging.info('Sending email %s-%s' % (to, subject))
    else:
        send_email(to, subject, body)


def async_send_admin_email(subject, body):
    async = str2bool(os.getenv('ASYNC_TASKS', True))
    if async:
        queue = connect_redis.default_queue()
        queue.enqueue(send_admin_email, subject, body)
        logging.info('Sending admin email %s' % subject)
    else:
        send_admin_email(subject, body)


def async_tweet(msg):
    test_mode = str2bool(os.getenv('TEST_MODE', False))
    if test_mode:
        logging.info('Tweeting {msg}'.format(msg=msg))
    else:
        async = str2bool(os.getenv('ASYNC_TASKS', True))
        if async:
            queue = connect_redis.default_queue()
            queue.enqueue(tweet, msg)
            logging.info('Tweeting %s' % msg)
        else:
            tweet(msg)


def get_lat_long_from_ip(ip):
    try:
        url = 'http://secret-ips.herokuapp.com/api/ip-city?ip=%s' % ip
        r = requests.get(url)
        r = r.json()
        return (float(r['latitude']), float(r['longitude']))
    except Exception as e:
        logging.error(str(e))
        raise e, None, sys.exc_info()[2]


def get_country_from_ip(ip):
    try:
        url = 'http://secret-ips.herokuapp.com/api/ip-country?ip=%s' % ip
        r = requests.get(url)
        r = r.json()
        country_code = r['country_code'].lower()
        return country_code
    except Exception as e:
        logging.error(str(e))


def add_contact_to_propagation(email=None, fb_id=None, tags=None, languages=None):
    if email or fb_id:
        domain = 'http://propagation.herokuapp.com'
        try:
            payload = {}
            if email:
                payload['email'] = email
            if fb_id:
                payload['fb_id'] = fb_id
            if tags:
                if isinstance(tags, (list, set)):
                    tags = ','.join(tags)
                payload['tags'] = tags
            if languages:
                if isinstance(languages, (list, set)):
                    languages = ','.join(languages)
                payload['languages'] = languages
            r = requests.post('%s/api/create-update-contact' % domain, data=payload)
            print('[%s] http POST /create-update-contact' % (r.status_code,))
        except KeyError as e:
            logging.exception(e)
