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


class ApiBaseHandler(BaseHandler):
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
        elif isinstance(data, dict):
            data_obj = {}
            for k, v in data.items():
                data_obj[k] = self.prepare_data(v)
            return data_obj
        elif is_iterable:
            return [self.prepare_data_obj(d) for d in data]
        return data

    def answer(self, data):
        self.set_header("Content-Type", "application/json")
        data_json = data_to_json(self.prepare_data(data))
        self.write(data_json)

    def answer_with_pagination(self, array):
        total_count = len(array)
        # limit E [10,1000]
        limit = int(self.get_argument('limit', 10))
        limit = min(1000, limit) if limit > 0 else max(10, limit)
        # initial E [0:count-1]
        initial = int(self.get_argument('initial', 0))
        initial = min(total_count-1, initial) if limit > 0 else max(0, limit)
        last_index = initial + limit
        results = array[initial:last_index]
        count = len(results)
        is_first_page = initial == 0
        is_last_page = last_index >= total_count
        next = 'initial=%s&limit=%s' % (last_index, limit) if not is_last_page else None
        previous = 'initial=%s&limit=%s' % (max(0, initial - limit), limit) if not is_first_page else None
        response = dict(total_count=total_count, count=count, results=results, next=next, previous=previous)
        # print(is_first_page, is_last_page)
        # print(initial, limit)
        # print(response)
        self.answer(response)

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


class ApiHandler(ApiBaseHandler):
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
