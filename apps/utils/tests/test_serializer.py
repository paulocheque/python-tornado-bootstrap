# coding: utf-8
import unittest

from mongoengine import *
from bson import Binary

from ..serializer import *


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
        document_to_data_obj(obj)

    def test_obj_with_binary(self):
        class X(Document):
            a = BinaryField()
        obj = X(a=u'abc')
        document_to_data_obj(obj)

    def test_obj_with_string_unicode(self):
        class X(Document):
            a = StringField()
        obj1 = X(a=u'\x80abc')
        document_to_data_obj(obj1)

    def test_obj_with_binary_unicode(self):
        class X(Document):
            a = BinaryField()
        obj1 = X(a=u'\x80abc')
        document_to_data_obj(obj1)


class DataToJsonTests(unittest.TestCase):
    def test_dict(self):
        self.assertEquals('{}', data_to_json({}))

    def test_lits_of_dicts(self):
        self.assertEquals('[]', data_to_json([]))
        self.assertEquals('[{}]', data_to_json([{}]))
        self.assertEquals('[{}, {}]', data_to_json([{}, {}]))

    def test_document(self):
        class X(Document):
            a = StringField()
        self.assertEquals('{"a": "123"}', data_to_json(X(a='123')))

    def test_document_with_binary(self):
        class X(Document):
            a = BinaryField()
        self.assertEquals(True, len(data_to_json(X(a=u'\x80123'))) > 20) # base64 string

    def test_list_of_documents(self):
        class X(Document):
            a = StringField()
        self.assertEquals('[{"a": "123"}, {"a": "123"}]', data_to_json([X(a='123'), X(a='123')]))

    def test_mixed_list(self):
        class X(Document):
            a = StringField()
        self.assertEquals('[{"a": "123"}, {}]', data_to_json([X(a='123'), {}]))

    def test_string(self):
        self.assertEquals('"x"', data_to_json('x'))
