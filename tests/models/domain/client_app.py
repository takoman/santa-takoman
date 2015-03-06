# -*- coding: utf-8 -*-

import unittest
from tests import AppTestCase
from mongoengine import *
from santa.models.domain import *
from tests.factories import *

class ClientAppsTests(AppTestCase):
    def setUp(self):
        super(ClientAppsTests, self).setUp()
        self.client_app = ClientAppFactory.create()

    def test_required_properties(self):
        with self.assertRaisesRegexp(ValidationError, ".*Field is required: \['name'\].*"):
            ClientApp().save()

    def test_defined_properties(self):
        for p in ['name', 'client_id', 'client_secret', 'token']:
            self.assertTrue(hasattr(self.client_app, p))

    def test_generate_id_and_secret_signal(self):
        client_app = ClientApp(name='Bear').save()
        # TODO: Need a better way to test the hex string
        self.assertEqual(len(client_app.client_id), 20)
        self.assertEqual(len(client_app.client_secret), 32)
        self.assertEqual(len(client_app.token), 128)

if __name__ == '__main__':
    unittest.main()
