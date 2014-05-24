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
        self.app = create_app()
        self.test_client = self.app.test_client()
        self.connection = None
        self.setupDB()

    def tearDown(self):
        self.dropDB()
        del self.app

    def setupDB(self):
        self.connection = MongoClient(self.app.config['MONGO_HOST'], self.app.config['MONGO_PORT'])
        self.db = self.connection[self.app.config['MONGO_DBNAME']]
        self.db.client_apps.insert({
            'client_id'     : 'rudy-test',
            'client_secret' : 'rudy-secret',
            'token'         : 'rudy-token'
            })
        self.db.users.insert({'id': 'takoman'})

    def dropDB(self):
        self.connection = MongoClient(self.app.config['MONGO_HOST'], self.app.config['MONGO_PORT'])
        self.connection.drop_database(self.app.config['MONGO_DBNAME'])
        self.connection.close()

if __name__ == '__main__':
    unittest.main()
