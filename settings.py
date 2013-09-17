# coding: utf-8
import os

DEBUG = False

if DEBUG:
    DOMAIN = 'localhost:5000'
else:
    DOMAIN = 'app.herokuapp.com'

TORNADO_SETTINGS = dict(
    gzip=True,
    debug=DEBUG,
    login_url='/login',
    post_login_redirect_url='/logged-in',
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    template_path='templates',
    autoescape=None,
    cookie_secret=os.environ.get('BSALT', 'your salt'),

    google_consumer_key='',
    google_consumer_secret='',

    facebook_redirect_uri='http://%s/auth/facebook' % DOMAIN,
    facebook_api_key='',
    facebook_secret='',

    github_redirect_uri='http://%s/auth/github' % DOMAIN,
    github_client_id='',
    github_secret='',
    github_scope='',

    twitter_consumer_key='',
    twitter_consumer_secret='',
)
