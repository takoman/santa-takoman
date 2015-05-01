# -*- coding: utf-8 -*-
from tests import AppTestCase
from santa.lib.user_trust import UserTrust
from bson.objectid import ObjectId
from santa.models.domain.user import User
from santa.models.domain.social_auth import SocialAuth
import unittest, json, datetime, dateutil.parser, mock

class AuthControllersTests(AppTestCase):

    def setUp(self):
        super(AuthControllersTests, self).setUp()
        User(name='Tako Man', email='takoman@takoman.co', password='password').save()
        self.user = User(name='Tako Woman',
                         email='takowoman@takoman.co').save()
        self.social_auth = SocialAuth(uid="10152476049619728",
                                      first_name="Woman",
                                      last_name="Tako",
                                      user=ObjectId(self.user.id),
                                      email="takowoman@takoman.co",
                                      name="Tako Woman").save()

    @unittest.skip("test is invalid password")
    def get_is_valid_password(self):
        pass

    def test_get_access_token_by_credentials(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='credentials',
            email='takoman@takoman.co',
            password='password'
        ))
        access_token = json.loads(rv.data).get('access_token')
        self.assertIsNotNone(access_token)
        with self.app.app_context():
            user = UserTrust().get_user_from_access_token({
                'access_token': access_token
            })
            self.assertIsNotNone(user)
            self.assertEqual(user.get('email'), 'takoman@takoman.co')

    def test_get_expires_in_by_credentials(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='credentials',
            email='takoman@takoman.co',
            password='password'
        ))
        res = json.loads(rv.data)
        self.assertIsNotNone(res.get('expires_in'))
        expires_in = dateutil.parser.parse(res.get('expires_in'))
        sixty_days_from_now = datetime.datetime.utcnow() + datetime.timedelta(days=60)
        # Heuristic, check the expires_in is roughly sixty days from now.
        self.assertLess((sixty_days_from_now - expires_in).seconds, 60)

    def test_get_access_token_missing_client_id(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_secret=self.client_app.client_secret,
            grant_type='credentials',
            email='takoman@takoman.co',
            password='password'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'), 'missing client_id')

    def test_get_access_token_invalid_client_id(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id='wrong',
            client_secret=self.client_app.client_secret,
            grant_type='credentials',
            email='takoman@takoman.co',
            password='password'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'), 'invalid client_id or client_secret')

    def test_get_access_token_invalid_client_secret(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret='wrong',
            grant_type='credentials',
            email='takoman@takoman.co',
            password='password'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'), 'invalid client_id or client_secret')

    def test_get_access_token_missing_email(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='credentials',
            password='password'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'), 'missing email')

    def test_get_access_token_missing_password(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='credentials',
            email='takoman@takoman.co'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'), 'missing password')

    def test_get_access_token_invalid_email(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='credentials',
            email='nobody@takoman.co',
            password='password'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'), 'invalid email or password')

    def test_get_access_token_invalid_login_type(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='credentials',
            email='takowoman@takoman.co',
            password='password'
        ))
        self.assertEqual(rv.status_code, 400)
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'), 'invalid login type')

    def test_get_access_token_invalid_password(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='credentials',
            email='takoman@takoman.co',
            password='thisisworng'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'), 'invalid email or password')

    # Since we use patterns like `from a import b`, b is actually a class in
    # the module, not the global scope. So patch directives need to refer to
    # my module, i.e. santa.apps.auth.controllers, not santa.lib.social_auth.
    # Compared to patterns like `import a` and use it like `a.b`
    # http://bhfsteve.blogspot.com/2012/06/patching-tip-using-mocks-in-python-unit.html
    @mock.patch('santa.apps.auth.controllers.SocialFacebook')
    def test_get_access_token_by_oauth_token(self, fb_mock):
        fb_instance = fb_mock.return_value
        fb_instance.get_auth_data.return_value = {
            'email'   : 'cy@takoman.co',
            'provider': 'facebook',
            'uid'     : '10152476049619728',
            'name'    : 'Chung-Yi Chi',
            'info'    : {
                'first_name': 'Chung-Yi',
                'last_name': 'Chi',
                'verified': True,
                'name': 'Chung-Yi Chi',
                'locale': 'en_US',
                'gender': 'male',
                'email': 'cy@takoman.co',
                'link': 'https://www.facebook.com/app_scoped_user_id/10152476049619728/',
                'timezone': -4,
                'updated_time': '2013-10-02T14:50:27+0000',
                'id': '10152476049619728'
            }
        }

        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='oauth_token',
            oauth_provider='facebook',
            oauth_token='facebook-oauth-token'
        ))
        access_token = json.loads(rv.data).get('access_token')
        self.assertIsNotNone(access_token)
        with self.app.app_context():
            user = UserTrust().get_user_from_access_token({
                'access_token': access_token
            })
            self.assertIsNotNone(user)
            self.assertEqual(user.get('email'), 'takowoman@takoman.co')

    @mock.patch('santa.apps.auth.controllers.SocialFacebook')
    def test_get_access_token_missing_oauth_provider(self, fb_mock):
        fb_instance = fb_mock.return_value
        fb_instance.get_auth_data.return_value = {
            'email'   : 'cy@takoman.co',
            'uid'     : '10152476049619728',
            'name'    : 'Chung-Yi Chi'
        }
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='oauth_token',
            oauth_token='facebook-oauth-token'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'), 'missing oauth provider')

    @mock.patch('santa.apps.auth.controllers.SocialFacebook')
    def test_get_access_token_missing_oauth_token(self, fb_mock):
        fb_instance = fb_mock.return_value
        fb_instance.get_auth_data.return_value = {
            'email'   : 'cy@takoman.co',
            'uid'     : '10152476049619728',
            'name'    : 'Chung-Yi Chi'
        }
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='oauth_token',
            oauth_provider='facebook'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'), 'missing oauth token')

    @mock.patch('santa.apps.auth.controllers.SocialFacebook')
    def test_get_access_token_unsupported_oauth_type(self, fb_mock):
        fb_instance = fb_mock.return_value
        fb_instance.get_auth_data.return_value = {
            'email'   : 'cy@takoman.co',
            'uid'     : '10152476049619728',
            'name'    : 'Chung-Yi Chi'
        }
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='oauth_token',
            oauth_provider='assbook',
            oauth_token='alienbook-oauth-token'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'), 'unsupported oauth provider')

    @mock.patch('santa.apps.auth.controllers.SocialFacebook')
    def test_get_access_token_invalid_oauth_token(self, fb_mock):
        fb_instance = fb_mock.return_value
        fb_instance.get_auth_data.return_value = None

        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='oauth_token',
            oauth_provider='facebook',
            oauth_token='facebook-oauth-token'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'), 'invalid oauth token')

    @mock.patch('santa.apps.auth.controllers.SocialFacebook')
    def test_get_access_token_no_matching_auth(self, fb_mock):
        fb_instance = fb_mock.return_value
        fb_instance.get_auth_data.return_value = {
            'email'   : 'cy@takoman.co',
            'uid'     : '1234',
            'name'    : 'Chung-Yi Chi'
        }
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='oauth_token',
            oauth_provider='facebook',
            oauth_token='facebook-oauth-token'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'),
                         'no account linked to oauth token, uid=1234, name=Chung-Yi Chi, email=cy@takoman.co')

    @mock.patch('santa.apps.auth.controllers.SocialFacebook')
    def test_get_access_token_matching_auth_no_user(self, fb_mock):
        # update social auth
        self.social_auth.user = None
        self.social_auth.save()

        fb_instance = fb_mock.return_value
        fb_instance.get_auth_data.return_value = {
            'email'   : 'cy@takoman.co',
            'uid'     : '10152476049619728',
            'name'    : 'Chung-Yi Chi'
        }
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='oauth_token',
            oauth_provider='facebook',
            oauth_token='facebook-oauth-token'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'),
                         'no account linked to oauth token, uid=10152476049619728, name=Chung-Yi Chi, email=cy@takoman.co')

    @mock.patch('santa.apps.auth.controllers.SocialFacebook')
    def test_get_access_token_matching_auth_no_matching_user(self, fb_mock):
        # remove the user from db
        self.user.delete()

        fb_instance = fb_mock.return_value
        fb_instance.get_auth_data.return_value = {
            'email'   : 'cy@takoman.co',
            'uid'     : '10152476049619728',
            'name'    : 'Chung-Yi Chi'
        }
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='oauth_token',
            oauth_provider='facebook',
            oauth_token='facebook-oauth-token'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'), 'missing user associated with this oauth token')

    def test_get_access_token_unsupported_grant_type(self):
        rv = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='wrong',
            email='takoman@takoman.co',
            password='password'
        ))
        res = json.loads(rv.data)
        self.assertEqual(res.get('message'), 'unsupported grant type')

if __name__ == '__main__':
    unittest.main()
