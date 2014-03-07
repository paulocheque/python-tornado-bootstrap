# coding: utf-8
import os

# heroku config:set VARIABLE=value
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

    google_api_key=os.environ.get('GOOGLE_API_KEY', ''),
    google_consumer_key=os.environ.get('GOOGLE_CONSUMER_KEY', ''),
    google_consumer_secret=os.environ.get('GOOGLE_CONSUMER_SECRET', ''),

    facebook_redirect_uri='http://%s/auth/facebook' % DOMAIN,
    facebook_api_key=os.environ.get('FACEBOOK_API_KEY', ''),
    facebook_secret=os.environ.get('FACEBOOK_SECRET', ''),

    github_redirect_uri='http://%s/auth/github' % DOMAIN,
    github_client_id=os.environ.get('GITHUB_CLIENT_ID', ''),
    github_secret=os.environ.get('GITHUB_SECRET', ''),
    github_scope=os.environ.get('GITHUB_SCOPE', ''),

    twitter_api_key=os.environ.get('TWITTER_API_KEY', ''),
    twitter_api_secret=os.environ.get('TWITTER_API_SECRET', ''),
    twitter_consumer_key=os.environ.get('TWITTER_CONSUMER_KEY', ''), # twitter_api_key
    twitter_consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET', ''), # twitter_api_secret
    twitter_access_token=os.environ.get('TWITTER_ACCESS_TOKEN', ''),
    twitter_access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', ''),
)

os.environ['GOOGLE_API_KEY'] = TORNADO_SETTINGS['google_api_key']

os.environ['FACEBOOK_API_KEY'] = TORNADO_SETTINGS['facebook_api_key']
os.environ['FACEBOOK_SECRET'] = TORNADO_SETTINGS['facebook_secret']
os.environ['FACEBOOK_API_SECRET'] = TORNADO_SETTINGS['facebook_secret']

os.environ['TWITTER_API_KEY'] = TORNADO_SETTINGS['twitter_api_key']
os.environ['TWITTER_API_SECRET'] = TORNADO_SETTINGS['twitter_api_secret']
os.environ['TWITTER_CONSUMER_KEY'] = TORNADO_SETTINGS['twitter_consumer_key']
os.environ['TWITTER_CONSUMER_SECRET'] = TORNADO_SETTINGS['twitter_consumer_secret']
os.environ['TWITTER_ACCESS_TOKEN'] = TORNADO_SETTINGS['twitter_access_token']
os.environ['TWITTER_ACCESS_TOKEN_SECRET'] = TORNADO_SETTINGS['twitter_access_token_secret']
