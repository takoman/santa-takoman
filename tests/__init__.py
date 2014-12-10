# -*- coding: utf-8 -*-
"""
    tests.test_base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    test base class
"""
import unittest, os
from santa import create_app
from santa.models.domain.client_app import ClientApp
from santa.models.domain.user import User

# Workaround to be able to use `mock.patch` decorator in Such DSL tests
def fix_case(f):
    def test(case):
        f(case=case)
    return test

class AppLifeCycle(object):
    description = 'Santa Test'

    @classmethod
    def setUp(cls):
        return

    @classmethod
    def tearDown(cls):
        return

    @classmethod
    def testSetUp(cls, test):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.environ['SANTA_SETTINGS'] = current_dir + '/../santa/config/settings_test.py'

        test.app = create_app()
        test.test_client = test.app.test_client()
        cls.dropDB(test)
        cls.setupDB(test)

    @classmethod
    def testTearDown(cls, test):
        cls.dropDB(test)
        del test.app

    @classmethod
    def setupDB(cls, test):
        ClientApp(client_id='rudy-test', client_secret='rudy-secret', token='rudy-token').save()

    @classmethod
    def dropDB(cls, test):
        # NOTE Now we can simply drop the entire database to reset the state.
        # https://github.com/MongoEngine/mongoengine/pull/823
        #
        # Previously we need to call Document.drop_collection() to properly
        # reset Mongoengine state.
        # https://github.com/MongoEngine/mongoengine/issues/812
        # for doc in [User, ClientApp, SocialAuth]:
        #     doc.drop_collection()
        test.app.db.drop_database(test.app.config['MONGO_DBNAME'])
        test.app.db.close()

class TestBase(unittest.TestCase):

    def setUp(self):
        # Set environment variable to override settings with test settings.
        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.environ['SANTA_SETTINGS'] = current_dir + '/../santa/config/settings_test.py'

        self.app = create_app()
        self.test_client = self.app.test_client()
        self.dropDB()
        self.setupDB()

    def tearDown(self):
        self.dropDB()
        del self.app

    def setupDB(self):
        ClientApp(client_id='rudy-test', client_secret='rudy-secret', token='rudy-token').save()
        User(name='Tako Man', email='takoman@takoman.co', password='password').save()

    def dropDB(self):
        # NOTE Now we can simply drop the entire database to reset the state.
        # https://github.com/MongoEngine/mongoengine/pull/823
        #
        # Previously we need to call Document.drop_collection() to properly
        # reset Mongoengine state.
        # https://github.com/MongoEngine/mongoengine/issues/812
        # for doc in [User, ClientApp, SocialAuth]:
        #     doc.drop_collection()
        self.app.db.drop_database(self.app.config['MONGO_DBNAME'])
        self.app.db.close()

if __name__ == '__main__':
    unittest.main()
