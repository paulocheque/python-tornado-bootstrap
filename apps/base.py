# coding: utf-8
import tornado.web

from apps.accounts.models import User


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        email = self.get_secure_cookie('user')
        if email is None:
            return None
        user = User.objects(email=email)
        try:
            return user[0]
        except IndexError:
            return None

    def render(self, template_name, **kwargs):
        if 'alert' not in kwargs:
            kwargs['alert'] = None
        if 'current_user' not in kwargs:
            kwargs['current_user'] = self.get_current_user()
        return super(BaseHandler, self).render(template_name, **kwargs)