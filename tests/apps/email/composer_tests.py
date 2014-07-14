# -*- coding: utf-8 -*-

from tests import TestBase
from santa.apps.email.models.composer import WelcomeEmailComposer
import unittest

class UsersTests(TestBase):

    def test_init_welcome_email_composer(self):
        composer = WelcomeEmailComposer('template.html')
        assert composer.template == 'template.html'

if __name__ == '__main__':
    unittest.main()
