# coding: utf-8
import unittest

from ..security import *


class GenerateSignatureTests(unittest.TestCase):
    def test_signature(self):
        self.assertEquals(generate_signature('1', {'a':1}), generate_signature('1', dict(a=1)))
        self.assertEquals(generate_signature('1', dict(a=u'áãàç')), generate_signature('1', dict(a='áãàç')))
        self.assertEquals(44, len(generate_signature('1', dict(a='a'))))
        self.assertEquals(44, len(generate_signature('1', dict(a='áãàç'))))
        self.assertEquals(44, len(generate_signature('1', dict(a=u'áãàç'))))
        self.assertEquals(44, len(generate_signature('1', dict(a=1.23))))


