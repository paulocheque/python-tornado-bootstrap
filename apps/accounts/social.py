import tornado.auth
import apps.accounts.handlers

from apps.accounts.models import User


class BaseSocialHandler(apps.accounts.handlers.AccountsHandler):
    def update_user(self, user, user_data):
        pass

    def _on_auth(self, user_data, email_label='email'):
        user, created = User.objects.get_or_create(email=user_data[email_label], auto_save=False)
        if created:
            self.update_user(user, user_data)
            user.save(validate=False)
        self.set_secure_cookie('user', user.email)
        return self.redirect(self.post_login_redirect_url())


class GoogleLoginHandler(BaseSocialHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("openid.mode", None):
            user_data = yield self.get_authenticated_user()
            self._on_auth(user_data)
        else:
            self.authenticate_redirect()

    def update_user(self, user, user_data):
        # https://developers.google.com/+/api/latest/people
        user.social = 'G'
        user.username = user_data.get('nickname', None)
        user.website_id = user_data.get('id', None)
        user.access_token = user_data.get("access_token", None)
        user.gender = user_data.get('gender', None)
        user.locale = user_data.get('language', None)


class FacebookLoginHandler(BaseSocialHandler, tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("code", False):
            user_data = yield self.get_authenticated_user(
                redirect_uri=self.settings['facebook_redirect_uri'],
                client_id=self.settings["facebook_api_key"],
                client_secret=self.settings["facebook_secret"],
                code=self.get_argument("code"))
            yield self.facebook_request("/me", access_token=user_data["access_token"], callback=self._on_auth)
        else:
            self.authorize_redirect(
                redirect_uri=self.settings['facebook_redirect_uri'],
                client_id=self.settings["facebook_api_key"],
                extra_params={"scope": "email"})

    def update_user(self, user, user_data):
        user.social = 'F'
        user.username = user_data.get('username', None)
        user.website_id = user_data.get('id', None)
        user.access_token = user_data.get("access_token", None)
        user.gender = user_data.get('gender', None)
        user.locale = user_data.get('locale', None)

