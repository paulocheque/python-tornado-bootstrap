# coding: utf-8
import unittest

from apps.utils.tests.base import MongoEngineTestCase
from ..models import *


class UserTests(unittest.TestCase):
    def test_valid_password(self):
        self.assertEquals(True, User.is_valid_password('asdASD123!@#'))
        self.assertEquals(False, User.is_valid_password('aA1#'))
        self.assertEquals(False, User.is_valid_password('aaaaaaaaaaa'))
        self.assertEquals(False, User.is_valid_password('AAAAAAAAAAA'))
        self.assertEquals(False, User.is_valid_password('11111111111'))
        self.assertEquals(False, User.is_valid_password('!!!!!!!!!!!'))
        self.assertEquals(False, User.is_valid_password('asdASD123!@# '))
