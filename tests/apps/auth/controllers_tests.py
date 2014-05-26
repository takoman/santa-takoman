# -*- coding: utf-8 -*-
from tests import TestBase
from santa.lib.user_trust import UserTrust
import unittest, json, datetime, dateutil.parser

class AuthControllersTests(TestBase):

    @unittest.skip("test is invalid password")
    def get_is_valid_password(self):
        pass

    def test_get_access_token_by_credentials(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id='rudy-test',
            client_secret='rudy-secret',
            grant_type='credentials',
            email='takoman@takoman.co',
            password='password'
        ))
        access_token = json.loads(rv.data).get('access_token')
        assert access_token is not None
        with self.app.app_context():
            user = UserTrust().get_user_from_access_token({
                'access_token': access_token
            })
            assert user is not None
            assert user.get('email') == 'takoman@takoman.co'

    def test_get_expires_in_by_credentials(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id='rudy-test',
            client_secret='rudy-secret',
            grant_type='credentials',
            email='takoman@takoman.co',
            password='password'
        ))
        res = json.loads(rv.data)
        assert res.get('expires_in') is not None
        expires_in = dateutil.parser.parse(res.get('expires_in'))
        sixty_days_from_now = datetime.datetime.now() + datetime.timedelta(days=60)
        # Heuristic, check the expires_in is roughly sixty days from now.
        assert (sixty_days_from_now - expires_in).seconds < 60

    def test_get_access_token_missing_client_id(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_secret='rudy-secret',
            grant_type='credentials',
            email='takoman@takoman.co',
            password='password'
        ))
        res = json.loads(rv.data)
        assert res.get('message') == 'missing client_id'

    def test_get_access_token_invalid_client_id(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id='wrong',
            client_secret='rudy-secret',
            grant_type='credentials',
            email='takoman@takoman.co',
            password='password'
        ))
        res = json.loads(rv.data)
        assert res.get('message') == 'invalid client_id or client_secret'

    def test_get_access_token_invalid_client_secret(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id='rudy-test',
            client_secret='wrong',
            grant_type='credentials',
            email='takoman@takoman.co',
            password='password'
        ))
        res = json.loads(rv.data)
        assert res.get('message') == 'invalid client_id or client_secret'

    def test_get_access_token_missing_email(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id='rudy-test',
            client_secret='rudy-secret',
            grant_type='credentials',
            password='password'
        ))
        res = json.loads(rv.data)
        assert res.get('message') == 'missing email'

    def test_get_access_token_missing_password(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id='rudy-test',
            client_secret='rudy-secret',
            grant_type='credentials',
            email='takoman@takoman.co'
        ))
        res = json.loads(rv.data)
        assert res.get('message') == 'missing password'

    def test_get_access_token_invalid_email(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id='rudy-test',
            client_secret='rudy-secret',
            grant_type='credentials',
            email='nobody@takoman.co',
            password='password'
        ))
        res = json.loads(rv.data)
        assert res.get('message') == 'invalid email or password'

    def test_get_access_token_invalid_password(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id='rudy-test',
            client_secret='rudy-secret',
            grant_type='credentials',
            email='takoman@takoman.co',
            password='thisisworng'
        ))
        res = json.loads(rv.data)
        assert res.get('message') == 'invalid email or password'

    def test_get_access_token_unsupported_grant_type(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id='rudy-test',
            client_secret='rudy-secret',
            grant_type='wrong',
            email='takoman@takoman.co',
            password='password'
        ))
        res = json.loads(rv.data)
        assert res.get('message') == 'unsupported grant type'

if __name__ == '__main__':
    unittest.main()
