# coding: utf-8

# http://www.tornadoweb.org/documentation/auth.html
# http://www.tornadoweb.org/documentation/websocket.html
from datetime import datetime

import tornado.web

from .models import *

from apps.utils.base import BaseHandler


class AccountsHandler(BaseHandler):
    def post_login_redirect_url(self):
        return self.get_argument('next', self.settings.get('post_login_redirect_url', '/'))


class RegisterHandler(AccountsHandler):
    def get(self):
        self.render('accounts/register.html', just_registered=False)

    def post(self):
        email = self.get_argument('email', None)
        pw = self.get_argument('password', None)

        if email is None or pw is None:
            self.render('accounts/register.html', alert='Email and password must not be blank.')
            return

        if len(User.objects(email=email)) > 0:
            self.render('accounts/register.html', alert='%s is already registered.' % email)
            return

        try:
            user = User(email=email, password=pw)
            user.save(encrypt_pass=True)
            self.set_secure_cookie('user', user.email)
            self.redirect(self.post_login_redirect_url())
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
        self.redirect(self.post_login_redirect_url())


class LogoutHandler(AccountsHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect(self.post_login_redirect_url())


class ResetPasswordHandler(AccountsHandler):
    def post(self):
        current_password = self.get_argument('current_password', None)
        new_password = self.get_argument('new_password', None)
        try:
            self.current_user.change_password(current_password, new_password)
            self.redirect(self.post_login_redirect_url(), alert='Password changed successfully')
        except ValidationError as e:
            self.render('accounts/user_page.html', alert=str(e))


class UserPageHandler(AccountsHandler):
    def get(self):
        self.render('accounts/user_page.html', alert=None)

