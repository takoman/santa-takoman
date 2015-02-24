# -*- coding: utf-8 -*-
"""
    tests.lib.user_trust_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    lib user_trust tests module
"""
import unittest, os, datetime
from tests import AppTestCase
from santa.models.domain.user import User
from santa.lib.user_trust import UserTrust
from santa.lib.api_errors import ApiException

class UserTrustTests(AppTestCase):

    def setUp(self):
        super(UserTrustTests, self).setUp()
        User(name='Tako Man', email='takoman@takoman.co', password='password').save()
        self.options = {
            'user': {'email': 'takoman@takoman.co'},
            'client_app': {'client_id': self.client_app.client_id},
            'expires_in': datetime.datetime.today() + datetime.timedelta(days=7)
        }

    def test_secret_key_missing_trust_key(self):
        if 'TOKEN_TRUST_KEY' in os.environ:
            del os.environ['TOKEN_TRUST_KEY']
        if 'TOKEN_TRUST_KEY' in self.app.config:
            del self.app.config['TOKEN_TRUST_KEY']
        with self.app.app_context():
            user_trust = UserTrust()
            self.assertRaisesRegexp(ApiException, "missing trust token key", user_trust.secret_key)

    @unittest.skip("Need to verify secret key valid.")
    def test_secret_key_sha256_hexdigest(self):
        pass

    def test_create_access_token_missing_user(self):
        self.options.pop("user", None)
        with self.app.app_context():
            user_trust = UserTrust()
            self.assertRaisesRegexp(ApiException, "missing user", user_trust.create_access_token, self.options)

    def test_get_user_from_access_token_missing_access_token(self):
        with self.app.app_context():
            user_trust = UserTrust()
            self.assertRaisesRegexp(ApiException, "missing access token", user_trust.get_user_from_access_token, {})

    def test_get_user_from_access_token_expired(self):
        self.options['expires_in'] = datetime.datetime.today() + datetime.timedelta(days=-1)
        with self.app.app_context():
            user_trust = UserTrust()
            access_token = user_trust.create_access_token(self.options)
            self.assertRaisesRegexp(ApiException, "token expired", user_trust.get_user_from_access_token, {'access_token': access_token})

    def test_get_user_from_access_token_missing_user_id(self):
        self.options['user'] = {'name': 'Takoman'}
        with self.app.app_context():
            user_trust = UserTrust()
            access_token = user_trust.create_access_token(self.options)
            self.assertRaisesRegexp(ApiException, "missing user_id", user_trust.get_user_from_access_token, {'access_token': access_token})

    def test_get_user_from_access_token_no_matching_app(self):
        self.options['client_app'] = {'client_id': 'invalid-app'}
        with self.app.app_context():
            user_trust = UserTrust()
            access_token = user_trust.create_access_token(self.options)
            user = user_trust.get_user_from_access_token({'access_token': access_token})
            self.assertIsNone(user)

    def test_get_user_from_access_token_no_matching_user(self):
        self.options['user'] = {'email': 'spiderman@takoman.co'}
        with self.app.app_context():
            user_trust = UserTrust()
            access_token = user_trust.create_access_token(self.options)
            user = user_trust.get_user_from_access_token({'access_token': access_token})
            self.assertIsNone(user)

    def test_create_access_token_and_extract_user_from_it(self):
        with self.app.app_context():
            user_trust = UserTrust()
            access_token = user_trust.create_access_token(self.options)
            user = user_trust.get_user_from_access_token({'access_token': access_token})
            self.assertEqual(user.get('email'), 'takoman@takoman.co')

    def test_create_utf8_access_token_and_extract_user_from_it(self):
        self.options = {
            'user': {u'email': u'takoman@takoman.co'},
            'client_app': {u'client_id': unicode(self.client_app.client_id, 'utf-8')},
            'expires_in': datetime.datetime.today() + datetime.timedelta(days=7)
        }
        with self.app.app_context():
            user_trust = UserTrust()
            access_token = user_trust.create_access_token(self.options)
            u_access_token = unicode(access_token, 'utf-8')
            user = user_trust.get_user_from_access_token({'access_token': u_access_token})
            self.assertIsNotNone(user)
            self.assertEqual(user.get('email'), 'takoman@takoman.co')

if __name__ == '__main__':
    unittest.main()
