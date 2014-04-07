# coding: utf-8
try:
    import simplejson as json
except ImportError:
    import json
# http://www.tornadoweb.org/documentation/escape.html
# tornado.escape.json_encode(value)[source]
import collections
from datetime import date, time, datetime

from mongoengine.base import BaseDocument
from mongoengine import *
from bson import Binary
from bson.objectid import ObjectId


class Serializable(object):
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)


# https://github.com/facebook/tornado/blob/master/tornado/util.py
class ObjectDict(dict):
    '''Makes a dictionary behave like an object, with attribute-style access.'''
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


class DefaultEncoder(json.JSONEncoder):
    def __init__(self, date_format='%Y/%m/%d', time_format='%H:%M', **kwargs): # FIXME: number of seconds
        super(DefaultEncoder, self).__init__(**kwargs)
        self.date_format = date_format
        self.time_format = time_format

    def default(self, obj):
        # print('DEFAULT ENCODER', type(obj), obj)
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, Binary):
            return str(obj).encode('base64')
        if isinstance(obj, datetime):
            return obj.strftime(self.date_format + ' ' + self.time_format)
        if isinstance(obj, date):
            return obj.strftime(self.date_format)
        if isinstance(obj, time):
            return obj.strftime(self.time_format)
        if isinstance(obj, type):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class DefaultDecoder(json.JSONDecoder):
    def __init__(self, date_format='%Y/%m/%d', time_format='%H:%M', **kwargs): # FIXME: number of seconds
        super(DefaultDecoder, self).__init__(**kwargs)
        self.date_format = date_format
        self.time_format = time_format

    def decode(self, string):
        # print string.__class__
        # if isinstance(obj, dict):
        #     return obj.__dict__
        return super(DefaultDecoder, self).decode(string)


def to_json(dicts, properties=None, encoder_class=DefaultEncoder):
    if isinstance(dicts, dict):
        for key, value in dicts.items():
            if isinstance(value, Binary):
                dicts[key] = str(value).encode('base64')
    elif isinstance(dicts, (str, unicode)):
        pass
    elif isinstance(dicts, (list, set)):
        for d in dicts:
            for key, value in d.items():
                if isinstance(value, Binary):
                    d[key] = str(value).encode('base64')
    return json.dumps(dicts, cls=encoder_class)


def from_json(dicts, properties=None, encoder_class=DefaultDecoder):
    return json.loads(dicts, cls=encoder_class)


def encodeBinaryAsBase64(document):
    for field, value in document._fields.items():
        if isinstance(value, BinaryField):
            encoded_value = str(str(value).encode('base64'))
            setattr(document, field, encoded_value)
    return document


def document_to_data_obj(document):
    document = encodeBinaryAsBase64(document)
    data_obj = dict(document.to_mongo()) if hasattr(document, 'to_mongo') else document
    return data_obj


def data_to_native_objects(data): # {}, [{}], Document or [Document]
    is_iterable = isinstance(data, collections.Iterable) and hasattr(data, '__iter__') and not hasattr(data, 'to_mongo')
    if isinstance(data, BaseDocument): # Document and EmbeddedDocument
        data_obj = document_to_data_obj(data)
    elif isinstance(data, dict):
        data_obj = {}
        for k, v in data.items():
            data_obj[k] = data_to_native_objects(v)
    elif isinstance(data, (str, unicode)):
        data_obj = data
    elif is_iterable:
        data_obj = [data_to_native_objects(d) for d in data]
    else:
        data_obj = data
    return data_obj


def data_to_json(data):
    data_obj = data_to_native_objects(data)
    return to_json(data_obj)


def to_dict(obj, properties=None, exclude=[]):
    if properties:
        d = vars(obj)
        result = {}
        for prop in properties:
            if prop in result.keys():
                result[prop] = d[prop]
    else:
        result = vars(obj)
    for prop in exclude:
        result.pop(prop, None)

    # for key, prop in result.iteritems():
    #     if not isinstance(prop, (str, unicode, list, set, dict, int, float)):
    #         print '::', key, prop
    return result

