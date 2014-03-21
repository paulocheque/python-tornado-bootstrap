# coding: utf-8
import tornado.web

from apps.utils.base import BaseHandler


class HomeHandler(BaseHandler):
    def get(self):
        style = self.get_argument('style', 'default')
        if style == 'print':
            template = 'app/main_print.html'
        elif style == 'noads':
            template = 'app/main_no_ads.html'
        else:
            template = 'app/main.html'

        if self.get_current_user():
            self.render(template)
        else:
            self.render(template, alert='You have to login first', alert_type='alert-info')
