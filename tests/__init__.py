# -*- coding: utf-8 -*-
"""
    tests.test_base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    test base class
"""
import unittest, os, bcrypt
from pymongo import MongoClient
from santa import create_app

class TestBase(unittest.TestCase):

    def setUp(self):
        # Set environment variable to override settings with test settings.
        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.environ['SANTA_SETTINGS'] = current_dir + '/../santa/config/settings_test.py'

        self.app = create_app()
        self.c = self.app.config  # set an alias for configs
        self.test_client = self.app.test_client()
        self.conn = None
        self.dropDB()
        self.setupDB()

    def tearDown(self):
        del self.app

    def setupDB(self):
        self.conn = MongoClient(self.c['MONGO_HOST'], self.c['MONGO_PORT'])
        self.db = self.conn[self.c['MONGO_DBNAME']]
        self.db.client_apps.insert({
            'client_id'     : 'rudy-test',
            'client_secret' : 'rudy-secret',
            'token'         : 'rudy-token'
        })
        hashed_password = bcrypt.hashpw('password', bcrypt.gensalt())
        self.db.users.insert({
            'name'    : 'Tako Man',
            'email'   : 'takoman@takoman.co',
            'password': hashed_password
        })

    def dropDB(self):
        self.conn = MongoClient(self.c['MONGO_HOST'], self.c['MONGO_PORT'])
        self.conn.drop_database(self.c['MONGO_DBNAME'])
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
