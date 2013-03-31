# coding: utf-8
import logging
import os
import sys

import tornado.ioloop
import tornado.web

from settings import *
import db # connect to databases
from tornado_rest_handler import routes, rest_routes

# apps
from apps.home import Home
from apps.admin import AdminMenu
from apps.accounts.handlers import *


logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='"%(asctime)s %(levelname)8s %(name)s - %(message)s"',
    datefmt='%H:%M:%S'
)

TORNADO_ROUTES = [
    (r'/?', Home),
    (r'/admin?', AdminMenu),


    (r"/register", RegisterHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/change_password", ResetPasswordHandler),
    (r"/account", UserPageHandler),

    # rest_routes(Example, prefix='examples', handler=CustomExampleHandler),

    (r'/.*\.(ico|png|jpg|gif|css|js|html)', tornado.web.StaticFileHandler, dict(path=os.path.dirname(__file__) + '/static')),
]

application = tornado.web.Application(routes(TORNADO_ROUTES), **TORNADO_SETTINGS)


if __name__ == "__main__":
    # http://www.tornadoweb.org/documentation/wsgi.html
    # to use with newrelic
    import newrelic.agent
    application = newrelic.agent.wsgi_application()(application)

    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
