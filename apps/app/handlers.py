# coding: utf-8
import tornado.web

from apps.utils.base import BaseHandler


class HomeHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.render('main.html')
        else:
            self.redirect('/', alert='You have to login first', alert_type='alert-info')
