# -*- coding: utf-8 -*-
import unittest, json
from tests import AppTestCase
from santa.models.domain.user import User

class MeControllersTests(AppTestCase):

    def setUp(self):
        super(MeControllersTests, self).setUp()
        User(name='Tako Man', email='takoman@takoman.co', password='password').save()

    def test_anonymous_user_access_me(self):
        res = self.test_client.get('/api/v1/me')
        self.assertEqual(res.status_code, 401)

    def test_invalid_access_token(self):
        res = self.test_client.get('/api/v1/me', headers={
            'X-ACCESS-TOKEN': 'invalid-access-token'
        })
        self.assertEqual(res.status_code, 401)

    @unittest.skip("Need to create expired access token")
    def test_expired_access_token(self):
        pass

    def test_access_token_in_header(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id='rudy-test',
            client_secret='rudy-secret',
            grant_type='credentials',
            email='takoman@takoman.co',
            password='password'
        ))
        access_token = json.loads(rv.data).get('access_token')
        rv = self.test_client.get('/api/v1/me', headers={
            'X-ACCESS-TOKEN': access_token
        })
        res = json.loads(rv.data)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(res.get('email'), 'takoman@takoman.co')

    def test_access_token_in_query_string(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id='rudy-test',
            client_secret='rudy-secret',
            grant_type='credentials',
            email='takoman@takoman.co',
            password='password'
        ))
        access_token = json.loads(rv.data).get('access_token')
        rv = self.test_client.get(
            '/api/v1/me?access_token=' + access_token)
        res = json.loads(rv.data)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(res.get('email'), 'takoman@takoman.co')

if __name__ == '__main__':
    unittest.main()
