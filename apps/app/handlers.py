# coding: utf-8
import tornado.web

from apps.accounts.handlers import AccountsHandler


class HomeHandler(AccountsHandler):
    def get(self):
        if self.get_current_user():
            self.render('main.html')
        else:
            self.render('main.html')
