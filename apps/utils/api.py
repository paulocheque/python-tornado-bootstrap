# coding: utf-8
import base64
import collections
import datetime
import hashlib
import hmac
import re

import tornado.web
from mongoengine.base import BaseDocument

from .base import BaseHandler
from .serializer import data_to_json
from apps.accounts.models import User # FIXME need refactoring


class ApiHandler(BaseHandler):
    def prepare_data_obj(self, data):
        if hasattr(data, 'to_api_dict'):
            identifier = None
            if hasattr(data, 'id'):
                identifier = str(data.id)
            data = data.to_api_dict()
            if identifier and 'id' not in data:
                data['id'] = identifier
                data['_id'] = identifier
            return data
        return data

    def prepare_data(self, data):
        is_iterable = isinstance(data, collections.Iterable) and hasattr(data, '__iter__') and not hasattr(data, 'to_mongo')
        if isinstance(data, BaseDocument):
            return self.prepare_data_obj(data)
        elif is_iterable:
            return [self.prepare_data_obj(d) for d in data]
        return data

    def answer(self, data):
        self.set_header("Content-Type", "application/json")
        data_json = data_to_json(self.prepare_data(data))
        self.write(data_json)

    def prepare(self):
        super(ApiHandler, self).prepare()
        self.authenticate()

    def authenticate(self):
        user = self.get_current_user()
        client_public_key = self.get_argument('auth_public_key', None)
        client_signature = self.get_argument('auth_signature', None)
        client_timestamp = self.get_argument('auth_timestamp', None)
        if user and client_public_key and client_signature and client_timestamp:
            # print("User id: " + str(user.id))
            # print("Public key: " + client_public_key)
            server_signature = self.get_signature(user.secret_key, self.get_request_string_data())
            # print("Client signature: " + client_signature)
            # print("Server signature: " + server_signature)
            if str(user.id) != client_public_key:
                print('401 for user id')
                self.raise401()
            if server_signature != client_signature:
                print('401 for signature')
                self.raise401()
            # TODO: timestamp validation: 10minutes
            # datetime.datetime.utcfromtimestamp(ms/1000.0)
            # datetime.datetime.utcnow()
        else:
            self.raise403()

    def get_signature(self, secret_key, data):
        data_prepared = []
        for key in sorted(data.keys()):
            value = data[key] if data[key] is not None else ''
            # https://api.jquery.com/serializeArray/
            # https://github.com/jquery/jquery/blob/master/src/serialize.js
            value = re.sub('\\s', '', value)
            token = key.lower() + "=" + value
            # print(token)
            data_prepared.append(token)
        data_prepared = '&'.join(data_prepared)
        string = '__'.join([self.request.method, self.request.path, data_prepared])
        string = string.encode('utf-8')
        secret_key = secret_key.encode('utf-8')
        # print("Data for signature: " + string)
        # print("Secret: " + secret_key)
        sha256hash = hmac.new(secret_key, string, digestmod=hashlib.sha256).digest()
        # print("SHA256 hash: " + sha256hash)
        signature = base64.b64encode(sha256hash);
        # print("Signature: " + signature)
        return signature

    def get_request_string_data(self):
        data = {}
        for arg in list(self.request.arguments.keys()):
            if arg in ['auth_version', 'auth_public_key', 'auth_timestamp', 'auth_signature']:
                continue
            data[arg] = self.get_argument(arg)
        return data

    def get_request_data(self):
        data = {}
        for arg in list(self.request.arguments.keys()):
            if arg in ['auth_version', 'auth_public_key', 'auth_timestamp', 'auth_signature']:
                continue
            data[arg] = self.get_argument(arg)
            if data[arg] == '': # Tornado 3.0+ compatibility
                data[arg] = None
            elif data[arg] and data[arg].lower() in ['false']:
                data[arg] = False
            elif data[arg] and data[arg].lower() in ['true']:
                data[arg] = True
        data['ip'] = self.request.remote_ip
        data['files'] = self.request.files
        data['user'] = self.get_current_user()
        return data
