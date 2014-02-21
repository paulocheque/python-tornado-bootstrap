# coding: utf-8
import logging
import os
import sys

import tornado.ioloop
import tornado.web

from settings import *
 # connect to databases
import connect_mongo
import connect_redis

# http://stackoverflow.com/questions/8143141/using-flask-and-tornado-together
from flask import Flask
from rq_dashboard import RQDashboard
rq_dashboard_app = Flask(__name__)
rq_dashboard_app.config['REDIS_URL'] = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
RQDashboard(rq_dashboard_app, '/rq')
tr = tornado.wsgi.WSGIContainer(rq_dashboard_app)

# apps
from apps.accounts.social import *
from apps.accounts.handlers import *
from apps.app.handlers import *


logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)8s %(name)s - %(message)s',
    datefmt='%H:%M:%S'
)

TORNADO_ROUTES = [
    (r'/?', Home),

    (r'/auth/facebook', FacebookLoginHandler),
    (r'/auth/google', GoogleLoginHandler),

    (r'/register', RegisterHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/change_password', ResetPasswordHandler),
    (r'/account', UserPageHandler),

    # (r'/api/model/?', ModelCrudHandler),
    # (r'/api/model/([0-9a-fA-F]{24,})/?', ModelCrudHandler),
    # (r'/api/model/count/?', ModelCrudHandler),

    (r'.*', tornado.web.FallbackHandler, dict(fallback=tr)),
]

application = tornado.web.Application(TORNADO_ROUTES, **TORNADO_SETTINGS)


if __name__ == '__main__':
    # http://www.tornadoweb.org/documentation/wsgi.html
    # to use with newrelic
    import newrelic.agent
    application = newrelic.agent.wsgi_application()(application)

    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
