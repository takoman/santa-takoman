# -*- coding: utf-8 -*-
"""
    tests.test_base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    test base class
"""
import unittest, json, os, datetime
from pymongo import MongoClient
from santa import create_app

class TestBase(unittest.TestCase):

    def setUp(self):
        # Set environment variable to override settings with test settings.
        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.environ['EVE_SETTINGS'] = current_dir+'/../config/settings_test.py'

        self.app = create_app()
        self.c = self.app.config # set an alias for configs
        self.test_client = self.app.test_client()
        self.conn = None
        self.setupDB()

    def tearDown(self):
        self.dropDB()
        del self.app

    def setupDB(self):
        self.conn = MongoClient(self.c['MONGO_HOST'], self.c['MONGO_PORT'])
        self.db = self.conn[self.c['MONGO_DBNAME']]
        self.db.client_apps.insert({
            'client_id'     : 'rudy-test',
            'client_secret' : 'rudy-secret',
            'token'         : 'rudy-token'
            })
        self.db.users.insert({'id': 'takoman'})

    def dropDB(self):
        self.conn = MongoClient(self.c['MONGO_HOST'], self.c['MONGO_PORT'])
        self.conn.drop_database(self.c['MONGO_DBNAME'])
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
