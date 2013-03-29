# coding: utf-8
import logging
import os
import sys

import tornado.ioloop
import tornado.web

from settings import *
import db # connect to databases

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


application = tornado.web.Application([
    (r'/?', Home),
    (r'/admin?', AdminMenu),

    (r"/register", RegisterHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/change_password", ResetPasswordHandler),
    (r"/account", UserPageHandler),

    # (r'/example/?', Example),
    # (r'/example/(\d{1,3})/?', Example),
    # (r'/example/([a-zA-Z0-9-]{3,20})/?', Example),

    (r'/(favicon\.ico)', tornado.web.StaticFileHandler, dict(path=os.path.dirname(__file__) + '/static')),
    (r'/.*\.(ico|png|jpg|gif|css|js|html)', tornado.web.StaticFileHandler, dict(path=os.path.dirname(__file__) + '/static')),
    ], **TORNADO_SETTINGS
)


if __name__ == "__main__":
    # http://www.tornadoweb.org/documentation/wsgi.html
    # to use with newrelic
    import newrelic.agent
    application = newrelic.agent.wsgi_application()(application)

    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
