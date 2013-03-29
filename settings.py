# coding: utf-8
import os

DEBUG = False


TORNADO_SETTINGS = dict(
    gzip=True,
    debug=DEBUG,
    login_url='/login',
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    template_path='templates',
    autoescape=None,
    cookie_secret=os.environ.get('BSALT', 'your salt'),
    twitter_consumer_key='',
    twitter_consumer_secret='',
    google_consumer_key='',
    google_consumer_secret='',
    facebook_api_key='',
    facebook_secret=''
)