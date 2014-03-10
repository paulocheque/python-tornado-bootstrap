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


def send_admin_mail(subject, body):
    try:
        sg = sendgrid.SendGridClient(os.getenv('SENDGRID_USERNAME'), os.getenv('SENDGRID_PASSWORD'))
        message = sendgrid.Mail(to='paulocheque@gmail.com',
            subject=subject,
            html=body,
            text=body,
            from_email='contact@paulocheque.com')
        sg.send(message)
    except Exception as e:
        logging.error(str(e))
        logging.exception(e)


def async_send_admin_mail(subject, body):
    queue = connect_redis.default_queue()
    queue.enqueue(send_admin_mail, subject, body)
    logging.info('Sending admin email %s' % subject)


def async_tweet(msg, debug=False):
    queue = connect_redis.default_queue()
    queue.enqueue(tweet, msg, debug=debug)
    logging.info('Tweeting %s' % msg)


def add_contact_to_propagation(email=None, fb_id=None, tags=None, languages=None, debug=False):
    if email or fb_id:
        if debug:
            domain = 'http://localhost:5000'
        else:
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
