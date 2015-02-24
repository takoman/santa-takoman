# -*- coding: utf-8 -*-
"""
    tests.api.users
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    api users tests module
"""
from tests import AppTestCase
from santa.models.domain.social_auth import SocialAuth
from santa.models.domain.user import User
import unittest, mock, json

# Need to patch the emailing services for all the tests to prevent sending
# "real" testing emails via Mandrill.
@mock.patch('santa.models.domain.user.MandrillAPI')
@mock.patch('santa.models.domain.user.WelcomeEmailComposer')
@mock.patch('santa.models.domain.user.Emailer')
class UsersEndpointsTests(AppTestCase):

    def setUp(self):
        super(UsersEndpointsTests, self).setUp()
        User(name='Tako Man', email='takoman@takoman.co', password='password').save()

    #
    # GET /users
    #

    def test_public_access_users(self, emailer_mock, composer_mock, mandrill_mock):
        res = self.test_client.get('/api/v1/users')
        self.assertEqual(res.status_code, 401)

    # TODO Test access control for different roles...

    #
    # POST /users
    #

    # Validation

    def test_create_user_by_credentials_duplicate_email(self, emailer_mock, composer_mock, mandrill_mock):
        user = {
            'name': 'takochan',
            'email': 'takochan@takoman.co',
            'password': 'takochanmansai'
        }
        res = self.test_client.post('/api/v1/users', data=user, headers={'X-XAPP-TOKEN': self.client_app_token})
        res = self.test_client.post('/api/v1/users', data=user, headers={'X-XAPP-TOKEN': self.client_app_token})

        self.assertEqual(res.status_code, 400)
        self.assertIn("duplicate unique keys", res.data)

    def test_create_user_by_credentialsi_unsupported_signup_type(self, emailer_mock, composer_mock, mandrill_mock):
        res = self.test_client.post('/api/v1/users', data=dict(
            email='takochan@takoman.co',
            password='takochanmansai'
        ), headers={'X-XAPP-TOKEN': self.client_app_token})

        self.assertEqual(res.status_code, 400)
        self.assertIn("unsupported signup type", res.data)

    def test_create_user_by_credentialsi_invalid_roles(self, emailer_mock, composer_mock, mandrill_mock):
        # TODO: In order to pass a list in the data, we have to send JSON.
        # Not sure how to do it with a form.
        res = self.test_client.post('/api/v1/users', data=json.dumps(dict(
            name='takochan',
            email='takochan@takoman.co',
            password='takochanmansai',
            role=['invalid-role']
        )), content_type="application/json", headers={'X-XAPP-TOKEN': self.client_app_token})

        self.assertEqual(res.status_code, 400)
        self.assertIn("Value must be one of", res.data)

    # Create by credentials

    def test_create_user_by_credentials(self, emailer_mock, composer_mock, mandrill_mock):
        res = self.test_client.post('/api/v1/users', data=dict(
            name='takochan',
            email='takochan@takoman.co',
            password='takochanmansai'
        ), headers={'X-XAPP-TOKEN': self.client_app_token})

        self.assertEqual(res.status_code, 201)
        self.assertIn('_id', res.data)

    def test_unauthorized_create_user_by_credentials(self, emailer_mock, composer_mock, mandrill_mock):
        res = self.test_client.post('/api/v1/users', data=dict(
            name='takochan',
            email='takochan@takoman.co',
            password='takochanmansai'
        ), headers={'X-XAPP-TOKEN': 'wrong-rudy-token'})

        self.assertEqual(res.status_code, 401)

    # Create by oauth tokens

    @mock.patch('santa.apps.api.v1.users.SocialFacebook')
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
        ), headers={'X-XAPP-TOKEN': self.client_app_token})

        self.assertEqual(res.status_code, 201)
        user = User.objects(email='kid@takoman.co').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'kid@takoman.co')
        self.assertEqual(user.name, 'Tako Kid')
        social_auth = SocialAuth.objects(user=user).first()
        self.assertIsNotNone(social_auth)
        self.assertEqual(social_auth.email, 'kid@takoman.co')
        self.assertEqual(social_auth.uid, '10152476049619728')
        self.assertEqual(social_auth.name, 'Tako-Kid')

    @mock.patch('santa.apps.api.v1.users.SocialFacebook')
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

        self.assertEqual(res.status_code, 401)

    # After creation hooks

    def test_send_welcome_email_after_create_user(self, emailer_mock, composer_mock, mandrill_mock):
        postman = mandrill_mock.return_value
        composer = composer_mock.return_value
        emailer_mock_instance = emailer_mock.return_value
        emailer_mock_instance.send_email = mock.Mock()
        res = self.test_client.post('/api/v1/users', data=dict(
            name='takochan',
            email='takochan@takoman.co',
            password='takochanmansai'
        ), headers={'X-XAPP-TOKEN': self.client_app_token})

        self.assertEqual(res.status_code, 201)
        self.assertTrue(emailer_mock.called)
        self.assertTrue(emailer_mock_instance.send_email.called)
        emailer_mock.assert_called_once_with(to_name='takochan',
                                             to_email='takochan@takoman.co',
                                             postman=postman,
                                             composer=composer)
        emailer_mock_instance.send_email.assert_called_once_with()

    def test_not_send_welcome_email_after_create_user_error(self, emailer_mock, composer_mock, mandrill_mock):
        emailer_mock_instance = emailer_mock.return_value
        emailer_mock_instance.send_email = mock.Mock()
        res = self.test_client.post('/api/v1/users', data=dict(
            name='takochan',
            email='takochan@takoman.co',
            password='takochanmansai'
        ), headers={'X-XAPP-TOKEN': 'wrong-rudy-token'})

        self.assertEqual(res.status_code, 401)
        self.assertFalse(emailer_mock.called)
        self.assertFalse(emailer_mock_instance.send_email.called)

if __name__ == '__main__':
    unittest.main()
