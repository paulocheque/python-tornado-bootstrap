# coding: utf-8
import os

def str2bool(string):
    if not string:
        return False
    if isinstance(string, (str, unicode)):
        string = string.lower()
        options = ['none', 'null', 'nil', 'false', 'f', 'no', '0']
        return not (string in options)
    return string

DEBUG = str2bool(os.environ.get('TEST_MODE', False))
ASYNC_TASKS = str2bool(os.environ.get('ASYNC_TASKS', True))
os.environ['TEST_MODE'] = str(DEBUG)
os.environ['ASYNC_TASKS'] = str(ASYNC_TASKS)

if DEBUG:
    print('='*80)
    print('RUNNING ON TEST MODE')
    print('='*80)
    os.environ['DATE_FORMAT'] = '%Y-%m-%d'
    os.environ['TIME_FORMAT'] = '%H:%M'
    os.environ['DATETIME_FORMAT'] = '{DATE_FORMAT} {TIME_FORMAT}'.format(
        DATE_FORMAT=os.environ['DATE_FORMAT'], TIME_FORMAT=os.environ['TIME_FORMAT'])

    os.environ['SYSTEM_NAME'] = 'MyApp'
    os.environ['DOMAIN'] = 'localhost:5000'
    os.environ['PROTOCOL'] = 'http'
    os.environ['SYSTEM_URL'] = '{PROTOCOL}://{DOMAIN}'.format(PROTOCOL=os.getenv('PROTOCOL'), DOMAIN=os.getenv('DOMAIN'))
    os.environ['SYSTEM_EMAIL'] = 'no-reply@{DOMAIN}'.format(DOMAIN=os.getenv('DOMAIN'))
    os.environ['ADMIN_EMAIL'] = 'paulocheque@gmail.com'
    os.environ['BSALT'] = '{DOMAIN}-yoursalt'.format(DOMAIN=os.environ['DOMAIN'])

    os.environ['GOOGLE_ANALYTICS'] = ''
    os.environ['GOOGLE_PLUS_ACCOUNT'] = ''
    os.environ['GOOGLE_API_KEY'] = ''
    os.environ['GOOGLE_CONSUMER_KEY'] = ''
    os.environ['GOOGLE_CONSUMER_SECRET'] = ''

    os.environ['FACEBOOK_ACCOUNT'] = ''
    os.environ['FACEBOOK_REDIRECT_URL'] = '{PROTOCOL}://{DOMAIN}/auth/facebook'.format(PROTOCOL=os.getenv('PROTOCOL'), DOMAIN=os.getenv('DOMAIN'))
    os.environ['FACEBOOK_API_KEY'] = ''
    os.environ['FACEBOOK_SECRET'] = ''
    os.environ['FACEBOOK_API_SECRET'] = os.environ['FACEBOOK_SECRET']

    os.environ['GITHUB_ACCOUNT'] = ''
    os.environ['GITHUB_REDIRECT_URL'] = '{PROTOCOL}://{DOMAIN}/auth/github'.format(PROTOCOL=os.getenv('PROTOCOL'), DOMAIN=os.getenv('DOMAIN'))
    os.environ['GITHUB_CLIENT_ID'] = ''
    os.environ['GITHUB_SECRET'] = ''
    os.environ['GITHUB_SCOPE'] = ''

    os.environ['TWITTER_ACCOUNT'] = ''
    os.environ['TWITTER_API_KEY'] = ''
    os.environ['TWITTER_API_SECRET'] = ''
    os.environ['TWITTER_CONSUMER_KEY'] = os.environ['TWITTER_API_KEY']
    os.environ['TWITTER_CONSUMER_SECRET'] = os.environ['TWITTER_API_SECRET']
    os.environ['TWITTER_ACCESS_TOKEN'] = ''
    os.environ['TWITTER_ACCESS_TOKEN_SECRET'] = ''

    os.environ['SKYPE_ACCOUNT'] = ''

    os.environ['PAGSEGURO_MODE'] = 'sandbox'
    os.environ['PAGSEGURO_EMAIL'] = ''
    os.environ['PAGSEGURO_TOKEN'] = ''
    os.environ['MERCADOPAGO_MODE'] = 'sandbox'
    os.environ['MERCADOPAGO_CLIENT_ID'] = ''
    os.environ['MERCADOPAGO_CLIENT_SECRET'] = ''
    os.environ['PAYPAL_MODE'] = 'sandbox'
    os.environ['PAYPAL_CLIENT_ID'] = ''
    os.environ['PAYPAL_CLIENT_SECRET'] = ''
    os.environ['MOIP_MODE'] = 'sandbox'
    os.environ['MOIP_TOKEN'] = ''
    os.environ['MOIP_KEY'] = ''
else:
    print('='*80)
    print('RUNNING ON PRODUCTION MODE')
    print('='*80)
    # heroku config:set VARIABLE=value


TORNADO_SETTINGS = dict(
    gzip=True,
    debug=DEBUG,
    login_url='/login',
    post_login_redirect_url='/',
    static_path=os.path.join(os.path.dirname(__file__), 'static'),
    template_path='templates',
    autoescape=None,
    cookie_secret=os.environ.get('BSALT'),

    google_api_key=os.environ.get('GOOGLE_API_KEY'),
    google_consumer_key=os.environ.get('GOOGLE_CONSUMER_KEY'),
    google_consumer_secret=os.environ.get('GOOGLE_CONSUMER_SECRET'),

    facebook_redirect_uri=os.environ.get('FACEBOOK_REDIRECT_URL'),
    facebook_api_key=os.environ.get('FACEBOOK_API_KEY'),
    facebook_secret=os.environ.get('FACEBOOK_SECRET'),

    github_redirect_uri=os.environ.get('GITHUB_REDIRECT_URL'),
    github_client_id=os.environ.get('GITHUB_CLIENT_ID'),
    github_secret=os.environ.get('GITHUB_SECRET'),
    github_scope=os.environ.get('GITHUB_SCOPE'),

    twitter_api_key=os.environ.get('TWITTER_API_KEY'),
    twitter_api_secret=os.environ.get('TWITTER_API_SECRET'),
    twitter_consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'), # twitter_api_key
    twitter_consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'), # twitter_api_secret
    twitter_access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
    twitter_access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'),
)
