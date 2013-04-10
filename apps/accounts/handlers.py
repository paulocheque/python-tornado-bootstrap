# coding: utf-8

# http://www.tornadoweb.org/documentation/auth.html
# http://www.tornadoweb.org/documentation/websocket.html
from datetime import datetime

import tornado.web
from tornado_rest_handler import TornadoRestHandler

from models import *


class AccountsHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        email = self.get_secure_cookie("user")
        if email is None:
            return None

        user = User.objects(email=email)

        try:
            return user[0]
        except IndexError:
            return None

    def render(self, template_name, **kwargs):
        kwargs['current_user'] = self.get_current_user()
        if 'alert' not in kwargs:
            kwargs['alert'] = None
        super(AccountsHandler, self).render(template_name, **kwargs)


class RestAccountsHandler(AccountsHandler, TornadoRestHandler):
    pass


class RegisterHandler(AccountsHandler):
    def get(self):
        self.render('accounts/register.html', just_registered=False)

    def post(self):
        email = self.get_argument('email', None)
        pw = self.get_argument('password', None)
        internal_password = self.get_argument('internal_password', None)

        if email is None or pw is None or internal_password is None:
            self.render('accounts/register.html', alert='Email and password must not be blank.')
            return

        if len(User.objects(email=email)) > 0:
            self.render('accounts/register.html', alert='%s is already registered.' % email)
            return

        try:
            user = User(email=email, password=pw, internal_password=internal_password)
            user.save(encrypt_pass=True)
            self.set_secure_cookie('user', user.email)
            self.redirect('/')
        except ValidationError as e:
            return self.render('accounts/register.html', alert=str(e))


class LoginHandler(AccountsHandler):
    def post(self):
        email = self.get_argument('email', None)
        pw = self.get_argument('password', None)

        user = User.authenticate(email=email, password=pw)
        if len(user) != 1:
            return self.render('accounts/register.html', alert='Bad login! Are you registered?')
        user = user[0]

        self.set_secure_cookie('user', user.email)
        self.redirect('/')


class LogoutHandler(AccountsHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect('/')


class ResetPasswordHandler(AccountsHandler):
    def post(self):
        current_password = self.get_argument('password_current', None)
        new_password = self.get_argument('password', None)
        try:
            self.current_user.change_password(current_password, new_password)
            self.redirect('/')
        except ValidationError as e:
            self.render('accounts/user_page.html', alert=str(e))


class UserPageHandler(AccountsHandler):
    def get(self):
        self.render('accounts/user_page.html', alert=None)

