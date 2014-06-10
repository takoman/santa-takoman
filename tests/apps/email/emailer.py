# -*- coding: utf-8 -*-

from tests import TestBase
from santa.apps.email.models.emailer import Emailer
import unittest, mock

class UsersTests(TestBase):

    def test_init_emailer_with_default_value(self):
        emailer = Emailer()
        assert emailer.to_name is None
        assert emailer.to_email is None
        assert emailer.from_name == 'Takoman (代購超人)'
        assert emailer.from_email == 'it@takoman.co'
        assert emailer.subject is None
        assert emailer.cc is None
        assert emailer.bcc is None
        assert emailer.reply_to == 'it@takoman.co'
        assert emailer.html is None
        assert emailer.sent_at is None
        assert emailer.postman_send_id is None
        assert emailer.postman is None
        assert emailer.composer is None

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

        assert emailer.to_name == 'Chung-Yi'
        assert emailer.to_email == 'chungyi@takoman.co'
        assert emailer.from_name == 'Takoman Support'
        assert emailer.from_email == 'support@takoman.co'
        assert emailer.subject == '歡迎使用 Takoman'
        assert emailer.cc == 'pingchieh@takoman.co'
        assert emailer.bcc == 'nick@takoman.co'
        assert emailer.reply_to == 'support@takoman.co'
        assert emailer.html == '<p>Welcome</p>'
        assert emailer.sent_at == '2014-06-08T18:58:51-0400'
        assert emailer.postman_send_id == '0001'
        assert emailer.postman == postman
        assert emailer.composer == composer

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

        assert emailer.create_message() == {
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
        }

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
