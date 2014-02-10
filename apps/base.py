# coding: utf-8
import tornado.web

from apps.accounts.models import User
import connect_redis

redis_connection = connect_redis.connect_to_redis()


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
        if 'alert_type' not in kwargs:
            kwargs['alert_type'] = None
        if 'current_user' not in kwargs:
            kwargs['current_user'] = self.get_current_user()
        return super(BaseHandler, self).render(template_name, **kwargs)


class CachedBaseHandler(BaseHandler):
    def prepare(self):
        cached = redis_connection.get(self.request.uri)
        if cached is not None:
            # print('Read cached page for %s' % self.request.uri)
            self.write(cached)
            self.finish()

    def render_string(self, template_name, **kwargs):
        html_generated = super(CacheBaseHandler, self).render_string(template_name, **kwargs)
        redis_connection.set(self.request.uri, html_generated)
        # print('Page %s cached' % self.request.uri)
        return html_generated
