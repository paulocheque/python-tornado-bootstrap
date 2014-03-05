# coding: utf-8
import unittest

from ..common import *


class SmartSplitTests(unittest.TestCase):
    def test_1(self):
        self.assertEquals(None, smart_split(None))
        self.assertEquals([], smart_split(''))
        self.assertEquals(['a'], smart_split('a'))
        self.assertEquals(['a'], smart_split(u'a'))
        self.assertEquals(['a'], smart_split(['a']))
        self.assertEquals(['a', 'b'], smart_split('a,b'))
        self.assertEquals(['a', 'b'], smart_split(u'a,b'))
        self.assertEquals(['a', 'b'], smart_split('a,b,'))
        self.assertEquals(['a', 'b'], smart_split(' a , b ,'))
        self.assertEquals(['a', 'b'], smart_split(' a , b , a,b'))


class ToLowerCaseTests(unittest.TestCase):
    def test_1(self):
        self.assertEquals(None, to_lower_case(None))
        self.assertEquals('', to_lower_case(''))
        self.assertEquals('aaa', to_lower_case('aaa'))
        self.assertEquals('aaa', to_lower_case('AAA'))
        self.assertEquals(['a', 'b'], to_lower_case(['A', 'B']))
