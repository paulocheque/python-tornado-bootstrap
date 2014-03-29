# coding: utf-8
from datetime import datetime, timedelta
import os
import unittest

from nose.tools import raises
from mongoengine import *

from apps.utils.tests.base import MongoEngineTestCase
from ..images import *


filepath = os.path.dirname(__file__) + '/favicon.gif'
invalid_image = 'https://fbcdn-sphotos-c-a.akamaihd.net/hphotos-ak-prn2/v/t1.0-9/c36.0.50.50/p50x50/1526750_768327503196505_738407239_n.jpg?oh=df830f4cecf10dcfa0605632afd5f6ff&oe=53B38D5B&__gda__=1402542708_d179bbead244ec601731d3dba4e63f44&access_token=126528804044664|3umNAsHuyfxCxu9Pk7DB2vK6Wf4'
image_url = 'http://www.baladasusp.com/static/img/usp/baladasusp_logo_line_very_small.png'

class MyDoc(Document):
    image = ImageField()


class MyDocTests(MongoEngineTestCase):
    def test_save_from_file(self):
        t = MyDoc()
        save_from_file(t.image, filepath)
        t.save()
        self.assertEquals(True, t.image is not None)
        self.assertEquals(True, t.image.size is not None)

    def test_save_from_url(self):
        t = MyDoc()
        save_from_url(t.image, image_url)
        t.save()
        self.assertEquals(True, t.image is not None)
        self.assertEquals(True, t.image.size is not None)

    def test_save_from_request(self):
        t = MyDoc()
        fileinfo = dict(body=open(filepath, 'r').read(), content_type='image/gif')
        save_from_request(t.image, fileinfo)
        t.save()
        self.assertEquals(True, t.image is not None)
        self.assertEquals(True, t.image.size is not None)

    @raises(Exception)
    def test_save_from_url_with_error(self):
        t = MyDoc()
        save_from_url(t.image, invalid_image)
        t.save()

    def test_save_from_url_with_placeholder(self):
        t = MyDoc()
        save_from_url(t.image, invalid_image, persist=True, place_holder_url=image_url)
        self.assertEquals(True, t.image is not None)
        self.assertEquals(True, t.image.size is not None)
