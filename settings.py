# coding: utf-8
import os

DEBUG = False

APP_NAME = 'Your App'

HEROKU_APP_NAME = ''
HEROKU_NEW_RELIC_ACCOUNT = ''
HEROKU_NEW_RELIC_APP = ''

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