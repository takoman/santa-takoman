# -*- coding: utf-8 -*-
"""
    tests.api.users
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    api users tests module
"""
from tests import TestBase
import unittest, mock

# Need to patch the emailing services for all the tests to prevent sending
# "real" testing emails via Mandrill.
@mock.patch('santa.MandrillAPI')
@mock.patch('santa.WelcomeEmailComposer')
@mock.patch('santa.Emailer')
class UsersTests(TestBase):

    def test_public_access_users(self, emailer_mock, composer_mock, mandrill_mock):
        res = self.test_client.get('/api/v1/users')
        assert res.status_code == 401

    # TODO Test access control for different roles...

    # TODO Test validation here...

    def test_send_welcome_email_after_create_user(self, emailer_mock, composer_mock, mandrill_mock):
        # postman = mandrill_mock.return_value
        # composer = composer_mock.return_value
        emailer_mock_instance = emailer_mock.return_value
        emailer_mock_instance.send_email = mock.Mock()
        res = self.test_client.post('/api/v1/users', data=dict(
            name='takochan',
            email='takochan@takoman.co',
            password='takochanmansai'
        ), headers={'X-XAPP-TOKEN': 'rudy-token'})

        assert res.status_code == 201
        assert emailer_mock.called
        assert emailer_mock_instance.send_email.called
        # TODO Not sure why the `assert_called_once_with` does not work
        # assert emailer_mock.assert_called_once_with(to_name='takochan',
        #                                             to_email='takochan@takoman.co',
        #                                             postman=postman,
        #                                             composer=composer)
        # assert emailer_mock_instance.send_email.assert_called_with()

    def test_not_send_welcome_email_after_create_user_error(self, emailer_mock, composer_mock, mandrill_mock):
        emailer_mock_instance = emailer_mock.return_value
        emailer_mock_instance.send_email = mock.Mock()
        res = self.test_client.post('/api/v1/users', data=dict(
            name='takochan',
            email='takochan@takoman.co',
            password='takochanmansai'
        ), headers={'X-XAPP-TOKEN': 'wrong-rudy-token'})

        assert res.status_code == 401
        assert not emailer_mock.called
        assert not emailer_mock_instance.send_email.called

    def test_create_user_by_credentials(self, emailer_mock, composer_mock, mandrill_mock):
        res = self.test_client.post('/api/v1/users', data=dict(
            name='takochan',
            email='takochan@takoman.co',
            password='takochanmansai'
        ), headers={'X-XAPP-TOKEN': 'rudy-token'})

        assert res.status_code == 201
        assert '_id' in res.data

    def test_unauthorized_create_user_by_credentials(self, emailer_mock, composer_mock, mandrill_mock):
        res = self.test_client.post('/api/v1/users', data=dict(
            name='takochan',
            email='takochan@takoman.co',
            password='takochanmansai'
        ), headers={'X-XAPP-TOKEN': 'wrong-rudy-token'})

        assert res.status_code == 401

    @mock.patch('santa.SocialFacebook')
    def test_create_user_by_oauth_tokens(self, fb_mock, emailer_mock, composer_mock, mandrill_mock):
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
    def test_unauthorized_create_user_by_oauth_tokens(self, fb_mock, emailer_mock, composer_mock, mandrill_mock):
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
