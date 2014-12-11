# -*- coding: utf-8 -*-

from tests import AppTestCase
from santa.apps.email.models.composer import WelcomeEmailComposer
import unittest

class UsersTests(AppTestCase):

    def test_init_welcome_email_composer(self):
        composer = WelcomeEmailComposer('template.html')
        self.assertEqual(composer.template, 'template.html')

if __name__ == '__main__':
    unittest.main()
