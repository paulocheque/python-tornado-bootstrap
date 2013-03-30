# coding: utf-8
import tornado.web

from apps.accounts.handlers import AccountsHandler

class Home(AccountsHandler):
    def get(self):
        self.render('main.html')

