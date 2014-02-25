# coding: utf-8
import unittest

from mongoengine.connection import connect, disconnect, get_connection


class MongoEngineTestCase(unittest.TestCase):
    mongodb_name = 'test-db'

    def setUp(self):
        # http://about.travis-ci.org/docs/user/database-setup/
        disconnect()
        connect(self.mongodb_name)
        print('Connected to test database: ' + self.mongodb_name)

    def tearDown(self):
        connection = get_connection()
        print('Drop test database: ' + self.mongodb_name)
        connection.drop_database(self.mongodb_name)
        print('Disconnect from test database: ' + self.mongodb_name)
        disconnect()
