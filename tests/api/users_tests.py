# -*- coding: utf-8 -*-
"""
    tests.api.users
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    api users tests module
"""
from tests import TestBase
import unittest, mock

class UsersTests(TestBase):

    def test_public_access_users(self):
        res = self.test_client.get('/api/v1/users')
        assert res.status_code == 401

    # Test access control for different roles...

    # Test validation here...

    def test_create_user_by_credentials(self):
        res = self.test_client.post('/api/v1/users', data=dict(
            name='takochan',
            email='takochan@takoman.co',
            password='takochanmansai'
        ), headers={'X-XAPP-TOKEN': 'rudy-token'})

        assert res.status_code == 201
        assert '_id' in res.data

    def test_unauthorized_create_user_by_credentials(self):
        res = self.test_client.post('/api/v1/users', data=dict(
            name='takochan',
            email='takochan@takoman.co',
            password='takochanmansai'
        ), headers={'X-XAPP-TOKEN': 'wrong-rudy-token'})

        assert res.status_code == 401

    @mock.patch('santa.SocialFacebook')
    def test_create_user_by_oauth_tokens(self, fb_mock):
        fb_instance = fb_mock.return_value
        fb_instance.get_auth_data.return_value = {
            'email'   : 'kid@takoman.co',
            'uid'     : '10152476049619728',
            'name'    : 'Tako-Kid',
            'info'    : {
                'email': 'kid@takoman.co',
                'name': 'Tako-Kid'
            }
        }
        res = self.test_client.post('/api/v1/users', data=dict(
            oauth_token='DWzojAv2dkr8Dd',
            provider='facebook',
            name='Tako Kid'
        ), headers={'X-XAPP-TOKEN': 'rudy-token'})

        assert res.status_code == 201
        with self.app.app_context():
            users = self.app.data.driver.db['users']
            user = users.find_one({'email': 'kid@takoman.co'})
            assert user is not None
            assert user.get('email') == 'kid@takoman.co'
            assert user.get('name') == 'Tako Kid'
            social_auths = self.app.data.driver.db['social_authentications']
            social_auth = social_auths.find_one({'user': user.get('_id')})
            assert social_auth is not None
            assert social_auth.get('email') == 'kid@takoman.co'
            assert social_auth.get('uid') == '10152476049619728'
            assert social_auth.get('name') == 'Tako-Kid'

    @mock.patch('santa.SocialFacebook')
    def test_unauthorized_create_user_by_oauth_tokens(self, fb_mock):
        fb_instance = fb_mock.return_value
        fb_instance.get_auth_data.return_value = {
            'email'   : 'kid@takoman.co',
            'uid'     : '10152476049619728',
            'name'    : 'Tako-Kid'
        }
        res = self.test_client.post('/api/v1/users', data=dict(
            oauth_token='DWzojAv2dkr8Dd',
            provider='facebook',
            name='Tako Kid'
        ), headers={'X-XAPP-TOKEN': 'wrong-rudy-token'})

        assert res.status_code == 401

if __name__ == '__main__':
    unittest.main()
