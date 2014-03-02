import logging
import os
import re
from StringIO import StringIO
import sys

import requests
import sendgrid


def get_lat_long_from_ip(ip):
    try:
        r = requests.get('http://secret-ips.herokuapp.com/api/ip-city?ip=%s' % ip)
        r = r.json()
        return (float(r['latitude']), float(r['longitude']))
    except KeyError as e:
        raise e, None, sys.exc_info()[2]


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
