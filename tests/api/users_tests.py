# -*- coding: utf-8 -*-
"""
    tests.api.users
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    api users tests module
"""
from tests import TestBase
import unittest, json

class UsersTests(TestBase):

    def test_public_access_users(self):
        res = self.test_client.get('/api/v1/users')
        assert res.status_code == 401

    # Test access control for different roles...

    # Test validation here...

    def test_create_user(self):
        res = self.test_client.post('/api/v1/users', data=dict(
            name='takochan',
            email='takochan@takoman.co',
            password='takochanmansai'
        ), headers={'X-XAPP-TOKEN': 'rudy-token'})

        assert res.status_code == 201
        assert '_id' in res.data

    def test_unauthorized_create_user(self):
        res = self.test_client.post('/api/v1/users', data=dict(
            name='takochan',
            email='takochan@takoman.co',
            password='takochanmansai'
        ), headers={'X-XAPP-TOKEN': 'wrong-rudy-token'})

        assert res.status_code == 401

if __name__ == '__main__':
    unittest.main()
