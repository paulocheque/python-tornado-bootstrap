# coding: utf-8
from datetime import datetime, timedelta
import unittest
from nose.tools import raises

from apps.utils.tests.base import MongoEngineTestCase
from ..models import *


class AlgorithmTests(unittest.TestCase):
    def test_(self):
        self.assertEquals(True, True)


class MyDocTests(MongoEngineTestCase):
    # @raises(Exception)
    def test_(self):
        t = MyDoc(email='a@a.com', name='TestXyz')
        t.save()
        self.assertEquals('test-xyz', t.slug)

    @raises(Exception)
    def test_raises(self):
        raise Exception()



