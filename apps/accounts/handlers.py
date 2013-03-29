# coding: utf-8

# http://www.tornadoweb.org/documentation/auth.html
# http://www.tornadoweb.org/documentation/websocket.html

import sha
from datetime import datetime

import tornado.web

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


class RegisterHandler(AccountsHandler):
    def get(self):
        self.render('register.html', just_registered=False, page='register')

    def post(self):
        email = self.get_argument('email', None)
        pw = self.get_argument('password', None)

        if email is None or pw is None:
            self.render('main.html')
            return

        if len(User.objects(email=email)) > 0:
            self.render('main.html', hey='%s is already registered' % email, page='register')
            return

        user = User(
            email=email,
            password=sha.sha(pw).hexdigest(),
            registered_on=datetime.utcnow()
        )
        user.save()

        # log them in by setting the cookie
        self.set_secure_cookie('user', user.email)
        self.render('register.html', just_registered=True, current_user=user, page='register')


class LoginHandler(AccountsHandler):
    def post(self):
        email = self.get_argument('email', None)
        pw = self.get_argument('password', None)

        if pw is not None:
            pw = sha.sha(pw).hexdigest()

        user = User.objects(email=email, password=pw)
        if len(user) != 1:
            self.render('main.html', hey='Bad login. Try again', page=None, tests=[])
            return
        user = user[0]
        self.set_secure_cookie('user', user.email)
        self.redirect('/')


class LogoutHandler(AccountsHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect('/')


class ResetPasswordHandler(AccountsHandler):
    def post(self):
        new_password = self.get_argument('password', None)
        current_password = self.get_argument('password_current', None)

        if new_password is not None and current_password is not None:
            if sha.sha(current_password).hexdigest() != self.current_user.password:
                alert_text = '<strong>FAILED:</strong> Your original password was invalid.'
            else:
                self.current_user.password = sha.sha(new_password).hexdigest()
                self.current_user.save()
                alert_text = 'Your password, public key, and private key have been changed!'
        else:
            alert_text = 'Password change failed!'
        self.render('user_page.html', page='account', alert=alert_text)


class UserPageHandler(AccountsHandler):
    def get(self):
        self.render('user_page.html', alert=None)