# -*- coding: utf-8 -*-

from tests import AppTestCase
from santa.apps.email.models.emailer import Emailer
import unittest, mock

class UsersTests(AppTestCase):

    def test_init_emailer_with_default_value(self):
        emailer = Emailer()
        self.assertIsNone(emailer.to_name)
        self.assertIsNone(emailer.to_email)
        self.assertEqual(emailer.from_name, 'Takoman (代購超人)')
        self.assertEqual(emailer.from_email, 'it@takoman.co')
        self.assertIsNone(emailer.subject)
        self.assertIsNone(emailer.cc)
        self.assertIsNone(emailer.bcc)
        self.assertEqual(emailer.reply_to, 'it@takoman.co')
        self.assertIsNone(emailer.html)
        self.assertIsNone(emailer.sent_at)
        self.assertIsNone(emailer.postman_send_id)
        self.assertIsNone(emailer.postman)
        self.assertIsNone(emailer.composer)

    def test_init_emailer_with_custom_value(self):
        postman = object()
        composer = object()
        emailer = Emailer(to_name='Chung-Yi',
                          to_email='chungyi@takoman.co',
                          from_name='Takoman Support',
                          from_email='support@takoman.co',
                          subject='歡迎使用 Takoman',
                          cc='pingchieh@takoman.co',
                          bcc='nick@takoman.co',
                          reply_to='support@takoman.co',
                          html='<p>Welcome</p>',
                          sent_at='2014-06-08T18:58:51-0400',
                          postman_send_id='0001',
                          postman=postman,
                          composer=composer)

        self.assertEqual(emailer.to_name, 'Chung-Yi')
        self.assertEqual(emailer.to_email, 'chungyi@takoman.co')
        self.assertEqual(emailer.from_name, 'Takoman Support')
        self.assertEqual(emailer.from_email, 'support@takoman.co')
        self.assertEqual(emailer.subject, '歡迎使用 Takoman')
        self.assertEqual(emailer.cc, 'pingchieh@takoman.co')
        self.assertEqual(emailer.bcc, 'nick@takoman.co')
        self.assertEqual(emailer.reply_to, 'support@takoman.co')
        self.assertEqual(emailer.html, '<p>Welcome</p>')
        self.assertEqual(emailer.sent_at, '2014-06-08T18:58:51-0400')
        self.assertEqual(emailer.postman_send_id, '0001')
        self.assertEqual(emailer.postman, postman)
        self.assertEqual(emailer.composer, composer)

    def test_create_message(self):
        class Composer(object):
            def get_email_params(self):
                return { 'subject': 'Hello world', 'ga_campaign': 'welcome' }

            def compose_email(self):
                return '<h1>Welcome</h1>'

        emailer = Emailer(to_name='Chung-Yi',
                          to_email='chungyi@takoman.co',
                          from_name='Takoman Support',
                          from_email='support@takoman.co',
                          subject='歡迎使用 Takoman',
                          html='<p>Welcome</p>',
                          composer=Composer())

        self.assertEqual(emailer.create_message(), {
            'to_name': 'Chung-Yi',
            'to_email': 'chungyi@takoman.co',
            'subject': '歡迎使用 Takoman',
            'from_name': 'Takoman Support',
            'from_email': 'support@takoman.co',
            'reply_to': 'it@takoman.co',
            'html': '<p>Welcome</p>',
            'track_clicks': True,
            'track_opens': True,
            'test': False,
            'ga_campaign': 'welcome'
        })

    def test_send_email_without_composer(self):
        postman = object()
        emailer = Emailer(postman=postman)

        self.assertRaisesRegexp(StandardError, "emailer needs to have a postman and a composer", emailer.send_email)

    def test_send_email_without_postman(self):
        composer = object()
        emailer = Emailer(composer=composer)

        self.assertRaisesRegexp(StandardError, "emailer needs to have a postman and a composer", emailer.send_email)

    def test_send_email_without_receipient(self):
        composer = object()
        postman = object()
        emailer = Emailer(composer=composer, postman=postman)

        message = {'subject': '歡迎', 'html': '<p>Welcome</p>'}
        emailer.create_message = mock.MagicMock(return_value=message)
        self.assertRaisesRegexp(StandardError, "email should have receipient email, subject, and body", emailer.send_email)

    def test_send_email_without_subject(self):
        composer = object()
        postman = object()
        emailer = Emailer(composer=composer, postman=postman)

        message = {'to_email': 'kevin@gmail.com', 'html': '<p>Welcome</p>'}
        emailer.create_message = mock.MagicMock(return_value=message)
        self.assertRaisesRegexp(StandardError, "email should have receipient email, subject, and body", emailer.send_email)

    def test_send_email_without_body(self):
        composer = object()
        postman = object()
        emailer = Emailer(composer=composer, postman=postman)

        message = {'subject': '歡迎', 'to_email': 'shiningclare@gmail.com'}
        emailer.create_message = mock.MagicMock(return_value=message)
        self.assertRaisesRegexp(StandardError, "email should have receipient email, subject, and body", emailer.send_email)

    def test_send_email(self):
        class Composer(object):
            def get_email_params(self):
                return { 'subject': 'Hello world', 'ga_campaign': 'welcome' }

            def compose_email(self):
                return '<h1>Welcome</h1>'

        class Postman(object):
            def send_email(self):
                return

        emailer = Emailer(to_name='Chung-Yi',
                          to_email='chungyi@takoman.co',
                          from_name='Takoman Support',
                          from_email='support@takoman.co',
                          subject='歡迎使用 Takoman',
                          html='<p>Welcome</p>',
                          composer=Composer(),
                          postman=Postman())

        emailer.postman.send_email = mock.MagicMock()
        emailer.send_email()
        emailer.postman.send_email.assert_called_with(**{
            'to_name': 'Chung-Yi',
            'to_email': 'chungyi@takoman.co',
            'subject': '歡迎使用 Takoman',
            'from_name': 'Takoman Support',
            'from_email': 'support@takoman.co',
            'reply_to': 'it@takoman.co',
            'html': '<p>Welcome</p>',
            'track_clicks': True,
            'track_opens': True,
            'test': False,
            'ga_campaign': 'welcome'
        })

if __name__ == '__main__':
    unittest.main()
