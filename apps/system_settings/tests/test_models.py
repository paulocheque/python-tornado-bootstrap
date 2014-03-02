# coding: utf-8
from datetime import datetime, timedelta
import unittest

from apps.utils.tests.base import MongoEngineTestCase
from ..models import *


class SystemSettingsTests(MongoEngineTestCase):
    def setUp(self):
        super(SystemSettingsTests, self).setUp()
        SystemSettings.memory_cache = None

    def test_get_creates_new_unique_object_automatically(self):
        self.assertEquals(0, SystemSettings.objects.count())
        ss = SystemSettings.get()
        self.assertEquals(1, SystemSettings.objects.count())
        ss = SystemSettings.get()
        self.assertEquals(1, SystemSettings.objects.count())

    def test_get_has_a_memory_cache(self):
        ss1 = SystemSettings.get()
        ss2 = SystemSettings.get()
        self.assertEquals(id(ss1), id(ss2))

    def test_refresh_avoid_memory_cache(self):
        ss1 = SystemSettings.get()
        ss1.max_emails_per_day = 33
        ss1.save()
        ss2 = SystemSettings.refresh()
        self.assertEquals(1, SystemSettings.objects.count())
        self.assertNotEquals(id(ss1), id(ss2))
        self.assertEquals(33, ss2.max_emails_per_day)

    def test_save_refresh_the_memory_cache(self):
        ss1 = SystemSettings.get()
        ss1.max_emails_per_day = 33
        ss1.save()
        ss2 = SystemSettings.get()
        self.assertEquals(1, SystemSettings.objects.count())
        self.assertNotEquals(id(ss1), id(ss2))
        self.assertEquals(33, ss2.max_emails_per_day)