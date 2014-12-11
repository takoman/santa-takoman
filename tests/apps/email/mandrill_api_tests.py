# -*- coding: utf-8 -*-

from tests import AppTestCase
from santa.apps.email.models.mandrill_api import MandrillAPI
import unittest, os, mock, mandrill

class MandrillAPITests(AppTestCase):

    def test_init_api_key_from_config(self):
        if 'MANDRILL_API_KEY' in os.environ:
            del os.environ['MANDRILL_API_KEY']
        with self.app.app_context():
            mandrill_api = MandrillAPI()
            self.assertEqual(mandrill_api.api_key, self.app.config.get('MANDRILL_API_KEY'))

    def test_init_api_key_env_override_config(self):
        os.environ['MANDRILL_API_KEY'] = 'api_key_from_env'
        with self.app.app_context():
            mandrill_api = MandrillAPI()
            self.assertEqual(mandrill_api.api_key, 'api_key_from_env')

    @mock.patch('santa.apps.email.models.mandrill_api.mandrill')
    def test_send_message_with_mandrill(self, md_mock):
        class M(object):
            def __init__(self):
                self.messages = mock.MagicMock()
                self.messages.send = mock.MagicMock()

        mandrill_stub = M()
        md_mock.Mandrill.return_value = mandrill_stub
        with self.app.app_context():
            mandrill_api = MandrillAPI()
            mandrill_api.send_email()
            mandrill_stub.messages.send.assert_called_once_with(message=mandrill_api.message, async=True)

    @mock.patch('santa.apps.email.models.mandrill_api.mandrill')
    def test_send_message_raise_mandrill_error(self, md_mock):
        md_mock.Mandrill = mock.Mock(side_effect=mandrill.Error('Boom!'))
        md_mock.Error = mandrill.Error
        with self.app.app_context():
            mandrill_api = MandrillAPI()
            self.assertRaisesRegexp(StandardError, "A mandrill error occurred:", mandrill_api.send_email)

if __name__ == '__main__':
    unittest.main()
