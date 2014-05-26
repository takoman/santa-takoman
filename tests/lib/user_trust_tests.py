# -*- coding: utf-8 -*-
"""
    tests.lib.user_trust_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    lib user_trust tests module
"""
import unittest, os, datetime
from tests import TestBase
from santa.lib.user_trust import UserTrust

class ClientAppsTests(TestBase):

    def test_secret_key_missing_trust_key(self):
        if 'TOKEN_TRUST_KEY' in os.environ:
            del os.environ['TOKEN_TRUST_KEY']
        if 'TOKEN_TRUST_KEY' in self.app.config:
            del self.app.config['TOKEN_TRUST_KEY']
        with self.app.app_context():
            user_trust = UserTrust()
            self.assertRaisesRegexp(StandardError, "missing trust token key", user_trust.secret_key)

    @unittest.skip("Need to verify secret key valid.")
    def test_secret_key_sha256_hexdigest(self):
        pass

    def test_create_access_token_missing_user(self):
        options = {
            'application': {'id': 'rudy-id'},
            'expires_in': datetime.datetime.today() + datetime.timedelta(days=7)
        }
        with self.app.app_context():
            user_trust = UserTrust()
            self.assertRaisesRegexp(StandardError, "missing user", user_trust.create_access_token, options)

    def test_get_user_from_access_token_missing_access_token(self):
        with self.app.app_context():
            user_trust = UserTrust()
            self.assertRaisesRegexp(StandardError, "missing access token", user_trust.get_user_from_access_token, {})

    def test_get_user_from_access_token_expired(self):
        options = {
            'user': {'id': 'takoman-id'},
            'application': {'id': 'rudy-id'},
            'expires_in': datetime.datetime.today() + datetime.timedelta(days=-1)
        }
        with self.app.app_context():
            user_trust = UserTrust()
            access_token = user_trust.create_access_token(options)
            self.assertRaisesRegexp(StandardError, "token expired", user_trust.get_user_from_access_token, {'access_token': access_token})

    def test_get_user_from_access_token_missing_user_id(self):
        options = {
            'user': {'name': 'Takoman'},
            'application': {'id': 'rudy-id'},
            'expires_in': datetime.datetime.today() + datetime.timedelta(days=1)
        }
        with self.app.app_context():
            user_trust = UserTrust()
            access_token = user_trust.create_access_token(options)
            self.assertRaisesRegexp(StandardError, "missing user_id", user_trust.get_user_from_access_token, {'access_token': access_token})

    def test_get_user_from_access_token_no_matching_app(self):
        options = {
            'user': {'id': 'takoman-id'},
            'application': {'id': 'invalid-app'},
            'expires_in': datetime.datetime.today() + datetime.timedelta(days=1)
        }
        with self.app.app_context():
            user_trust = UserTrust()
            access_token = user_trust.create_access_token(options)
            user = user_trust.get_user_from_access_token({'access_token': access_token})
            assert user is None

    def test_get_user_from_access_token_no_matching_user(self):
        options = {
            'user': {'id': 'spider-man'},
            'application': {'id': 'rudy-id'},
            'expires_in': datetime.datetime.today() + datetime.timedelta(days=1)
        }
        with self.app.app_context():
            user_trust = UserTrust()
            access_token = user_trust.create_access_token(options)
            user = user_trust.get_user_from_access_token({'access_token': access_token})
            assert user is None

    def test_create_access_token_and_extract_user_from_it(self):
        options = {
            'user': {'id': 'takoman-id'},
            'application': {'id': 'rudy-id'},
            'expires_in': datetime.datetime.today() + datetime.timedelta(days=7)
        }
        with self.app.app_context():
            user_trust = UserTrust()
            access_token = user_trust.create_access_token(options)
            user = user_trust.get_user_from_access_token({'access_token': access_token})
            assert user.get('email') == 'takoman@takoman.co'

    def test_create_utf8_access_token_and_extract_user_from_it(self):
        options = {
            'user': {u'id': u'takoman-id'},
            'application': {u'id': u'rudy-id'},
            'expires_in': datetime.datetime.today() + datetime.timedelta(days=7)
        }
        with self.app.app_context():
            user_trust = UserTrust()
            access_token = user_trust.create_access_token(options)
            u_access_token = unicode(access_token, 'utf-8')
            user = user_trust.get_user_from_access_token({'access_token': u_access_token})
            assert user.get('email') == 'takoman@takoman.co'

if __name__ == '__main__':
    unittest.main()
