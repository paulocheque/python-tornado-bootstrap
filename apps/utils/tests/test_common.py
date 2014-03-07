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
        self.assertEquals(['a', 'A', 'B', 'b'], smart_split(' a , B , A,b'))
        self.assertEquals(['a', 'A', 'B', 'b'], smart_split(' a \n B \n A\r\nb', comma='\n'))


class ToLowerCaseTests(unittest.TestCase):
    def test_1(self):
        self.assertEquals(None, to_lower_case(None))
        self.assertEquals('', to_lower_case(''))
        self.assertEquals('aaa', to_lower_case('aaa'))
        self.assertEquals('aaa', to_lower_case('AAA'))
        self.assertEquals(['a', 'b'], to_lower_case(['A', 'B']))


class TaggifyTests(unittest.TestCase):
    def test_accepts_strings(self):
        self.assertEquals(None, taggify(None))
        self.assertEquals([], taggify(''))
        self.assertEquals(['a'], taggify('a'))
        self.assertEquals(['a'], taggify(u'a'))
        self.assertEquals(['a'], taggify(['a']))
        self.assertEquals(['a', 'b'], taggify('a,b'))
        self.assertEquals(['a', 'b'], taggify(u'a,b'))
        self.assertEquals(['a', 'b'], taggify('a,b,'))
        self.assertEquals(['a', 'b'], taggify(' a , b ,'))
        self.assertEquals(['a', 'b'], taggify(' a , b , a,b'))
        self.assertEquals(['a', 'b'], taggify(' a , B , A,b'))
        self.assertEquals(['a', 'b'], taggify(' a \n B \n A\r\nb', comma='\n'))

    def test_accepts_lists(self):
        self.assertEquals(None, taggify(None))
        self.assertEquals([], taggify(['']))
        self.assertEquals(['a'], taggify(['a']))
        self.assertEquals(['a'], taggify([u'a']))
        self.assertEquals(['a'], taggify(['a']))
        self.assertEquals(['a', 'b'], taggify(['a', 'b']))
        self.assertEquals(['a', 'b'], taggify([u'a', u'b']))
        self.assertEquals(['a', 'b'], taggify([' a ',' b ',' a', 'b']))
        self.assertEquals(['a', 'b'], taggify([' a ',' B ',' A', 'b']))
