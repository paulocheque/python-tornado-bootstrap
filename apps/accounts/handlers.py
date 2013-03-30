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

    def render(self, template_name, **kwargs):
        kwargs['current_user'] = self.get_current_user()
        if 'alert' not in kwargs:
            kwargs['alert'] = None
        super(AccountsHandler, self).render(template_name, **kwargs)


class RegisterHandler(AccountsHandler):
    def get(self):
        self.render('accounts/register.html', just_registered=False)

    def post(self):
        email = self.get_argument('email', None)
        pw = self.get_argument('password', None)

        if email is None or pw is None:
            self.render('accounts/register.html', alert='Email and password must not be blank')
            return

        if len(User.objects(email=email)) > 0:
            self.render('accounts/register.html', alert='%s is already registered' % email)
            return

        user = User(
            email=email,
            password=sha.sha(pw).hexdigest(),
            registered_on=datetime.utcnow()
        )
        user.save()

        # log them in by setting the cookie
        self.set_secure_cookie('user', user.email)
        self.redirect('/')


class LoginHandler(AccountsHandler):
    def post(self):
        email = self.get_argument('email', None)
        pw = self.get_argument('password', None)

        if pw is not None:
            pw = sha.sha(pw).hexdigest()

        user = User.objects(email=email, password=pw)
        if len(user) != 1:
            self.render('accounts/register.html', alert='Bad login! Are you registered?')
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
        self.render('accounts/user_page.html', alert=alert_text)


class UserPageHandler(AccountsHandler):
    def get(self):
        self.render('accounts/user_page.html', alert=None)


class CrudHandler(AccountsHandler):
    def template_dir(self):
        return 'tornado_crud/'

    def obj_type(self):
        return None

    def fields(self):
        return [k for k,v in User._fields.iteritems() if v.required]

    def exclude(self):
        return []

    def objs(self):
        return self.obj_type().objects

    def obj(self, obj_id):
        return self.obj_type().objects.filter(id=obj_id).first()

    def render(self, template_name, **kwargs):
        super(CrudHandler, self).render(self.template_dir() + template_name, **kwargs)

    def get(self, obj_id=None, edit=False):
        if self.request.uri.endswith('/new'):
            self.render('edit.html', obj=None)
        if obj_id:
            obj = self.obj(obj_id)
            if obj:
                if edit:
                    self.render('edit.html', obj=obj)
                else:
                    data = self.get_arguments('obj_data')
                    self.render('show.html', obj=obj)
            else:
                self.render('list.html', objs=self.objs(), message='Object not found')
        else:
            self.render('list.html', objs=self.objs())

    def put(self, obj_id):
        data = self.get_argument('obj_data')
        obj = self.obj(obj_id)
        if obj:
            self.render(self.template_dir + 'list.html')
        else:
            raise tornado.web.HTTPError(404, 'Object not found')

    def post(self):
        data = self.get_argument('obj_data')
        success = True
        if success:
            self.render(self.template_dir + 'list.html', message='Object added successfully')
        else:
            self.render(self.template_dir + 'edit.html', obj=obj, errors=[])

    def delete(self, obj_id):
        obj = self.obj(obj_id)
        if obj:
            self.render('list.html', message='Object deleted successfully')
        else:
            raise tornado.web.HTTPError(404, 'Object not found')

