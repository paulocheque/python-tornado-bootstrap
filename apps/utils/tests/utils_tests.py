# coding: utf-8
import unittest

from mongoengine import *
from bson import Binary

from utils import *


class SerializableTests(unittest.TestCase):
    def test_update(self):
        x = Serializable(y=2)
        self.assertEquals(x.y, 2)


class ObjectDictTests(unittest.TestCase):
    def test_behavior(self):
        o = ObjectDict()
        o['x'] = 1
        self.assertEquals(o.x, 1)


class ToJsonTests(unittest.TestCase):
    def test_to_json_of_list(self):
        j = to_json([dict(a=1), dict(b='2'), dict(c=u'3')])

    def test_to_json_of_dict(self):
        j = to_json(dict(a=1, b='2', c=u'3'))

    def test_to_json_with_binary(self):
        j = to_json(dict(a=Binary('1')))
        j = to_json([dict(a=Binary('1'))])
        j = to_json(dict(a=Binary('1')), encoder_class=None)
        j = to_json([dict(a=Binary('1'))], encoder_class=None)

    def test_datetime(self):
        from datetime import datetime, date, time
        to_json(dict(a=datetime.now()))
        to_json(dict(a=datetime.today()))
        to_json(dict(a=time()))

    def test_object_dict(self):
        j = to_json(ObjectDict())


class DocumentToJsonTests(unittest.TestCase):
    def test_basic_obj(self):
        class X(Document):
            a = StringField()
        obj = X(a=u'abc')
        documents_to_json(obj)

    def test_list_of_objects(self):
        class X(Document):
            a = StringField()
        obj1 = X(a=u'abc')
        obj2 = X(a=u'abc')
        documents_to_json([obj1, obj2])

    def test_obj_with_binary(self):
        class X(Document):
            a = BinaryField()
        obj = X(a=u'abc')
        documents_to_json(obj)

    def test_obj_with_string_unicode(self):
        class X(Document):
            a = StringField()
        obj1 = X(a=u'\x80abc')
        obj2 = X(a=u'\x80abc')
        documents_to_json(obj1)
        documents_to_json([obj1, obj2])

    def test_obj_with_binary_unicode(self):
        class X(Document):
            a = BinaryField()
        obj1 = X(a=u'\x80abc')
        obj2 = X(a=u'\x80abc')
        documents_to_json(obj1)
        documents_to_json([obj1, obj2])
