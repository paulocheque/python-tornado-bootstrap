# coding: utf-8
import os

DEBUG = False

if DEBUG:
    DOMAIN = 'localhost:5000'
else:
    DOMAIN = os.environ.get('APP_DOMAIN', 'yourapp.herokuapp.com')

TORNADO_SETTINGS = dict(
    gzip=True,
    debug=DEBUG,
    login_url='/login',
    post_login_redirect_url='/',
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    template_path='templates',
    autoescape=None,
    cookie_secret=os.environ.get('BSALT', 'your salt'),

    google_consumer_key=os.environ.get('GOOGLE_CONSUMER_KEY', ''),
    google_consumer_secret=os.environ.get('GOOGLE_CONSUMER_SECRET', ''),

    facebook_redirect_uri='http://%s/auth/facebook' % DOMAIN,
    facebook_api_key=os.environ.get('FACEBOOK_API_KEY', ''),
    facebook_secret=os.environ.get('FACEBOOK_SECRET', '')

    github_redirect_uri='http://%s/auth/github' % DOMAIN,
    github_client_id=os.environ.get('GITHUB_CLIENT_ID', ''),
    github_secret=os.environ.get('GITHUB_SECRET', ''),
    github_scope=os.environ.get('GITHUB_SCOPE', ''),

    twitter_consumer_key=os.environ.get('TWITTER_CONSUMER_KEY', ''),
    twitter_consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET', ''),
)
