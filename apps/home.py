# coding: utf-8
import tornado.web


class Home(tornado.web.RequestHandler):
    def get(self):
        self.render('main.html')

