# coding: utf-8
import urllib

import tornado.web

from apps.accounts.models import User
import connect_redis

redis_connection = connect_redis.connect_to_redis()


class BaseHandler(tornado.web.RequestHandler):
    def check_permission(self, action):
        user = self.get_current_user()
        admin = self.is_admin_user()
        if action in self.perm_public or (user and action in self.perm_user) or (admin and action in self.perm_admin):
            pass # ok
        else:
            self.raise403()

    def raise401(self):
        raise tornado.web.HTTPError(401, 'Not enough permissions to perform this action')

    def raise403(self):
        raise tornado.web.HTTPError(403, 'Not enough permissions to perform this action')

    def raise404(self):
        raise tornado.web.HTTPError(404, 'Object not found')

    def get_current_user(self):
        email = self.get_secure_cookie('user')
        if email is None:
            return None
        return User.objects(email=email).first()

    def is_admin_user(self):
        user = self.get_current_user()
        return user and user.admin

    def redirect(self, url, alert=None, alert_type=None, permanent=False, status=None):
        if alert:
            alert = urllib.pathname2url(alert)
            url = '%s?alert=%s' % (url, alert)
            if alert_type:
                url = '%s&alert_type=%s' % (url, alert_type)
        super(BaseHandler, self).redirect(url, permanent=permanent, status=status)

    def render(self, template_name, **kwargs):
        if 'alert' not in kwargs:
            kwargs['alert'] = self.get_argument('alert', None)
        if 'alert_type' not in kwargs:
            # alert-success, alert-info, alert-warning, alert-danger
            kwargs['alert_type'] = self.get_argument('alert_type', 'alert-info')
        if 'current_user' not in kwargs:
            kwargs['current_user'] = self.get_current_user()
        return super(BaseHandler, self).render(template_name, **kwargs)


class CachedBaseHandler(BaseHandler):
    expire_timeout = 60 * 60 * 24 # in seconds

    def prepare(self):
        super(CachedBaseHandler, self).prepare()
        dev_mode = 'localhost' in self.request.host
        ignore_cache = self.get_argument('ignore_cache', None)
        if not ignore_cache and not dev_mode:
            cached = redis_connection.get(self.request.uri)
            if cached is not None:
                # print('Read cached page for %s' % self.request.uri)
                self.write(cached)
                self.finish()

    def render_string(self, template_name, **kwargs):
        html_generated = super(CachedBaseHandler, self).render_string(template_name, **kwargs)
        # redis_connection.setex(self.request.uri, self.expire_timeout, html_generated)
        redis_connection.set(self.request.uri, html_generated)
        redis_connection.expire(self.request.uri, self.expire_timeout)
        # print('Page %s cached' % self.request.uri)
        return html_generated
