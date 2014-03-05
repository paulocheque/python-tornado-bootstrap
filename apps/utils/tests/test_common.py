# coding: utf-8
import unittest

from ..common import *


class SplitByCommansTests(unittest.TestCase):
    def test_1(self):
        self.assertEquals(None, split_by_commas(None))
        self.assertEquals([], split_by_commas(''))
        self.assertEquals(['a'], split_by_commas('a'))
        self.assertEquals(['a'], split_by_commas(u'a'))
        self.assertEquals(['a'], split_by_commas(['a']))
        self.assertEquals(['a', 'b'], split_by_commas('a,b'))
        self.assertEquals(['a', 'b'], split_by_commas(u'a,b'))
        self.assertEquals(['a', 'b'], split_by_commas('a,b,'))
        self.assertEquals(['a', 'b'], split_by_commas(' a , b ,'))


class ToLowerCaseTests(unittest.TestCase):
    def test_1(self):
        self.assertEquals(None, to_lower_case(None))
        self.assertEquals('', to_lower_case(''))
        self.assertEquals('aaa', to_lower_case('aaa'))
        self.assertEquals('aaa', to_lower_case('AAA'))
        self.assertEquals(['a', 'b'], to_lower_case(['A', 'B']))
