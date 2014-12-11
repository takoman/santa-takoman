# -*- coding: utf-8 -*-
"""
    tests.api.client_apps_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    api client_apps tests module
"""
from tests import AppTestCase
import unittest, json

class ClientAppsTests(AppTestCase):

    def test_access_public_xapp_token(self):
        res = self.test_client.get('/api/v1/xapp_token')
        self.assertEqual(res.status_code, 200)

    def test_get_xapp_token(self):
        query = { 'client_id': 'rudy-test', 'client_secret': 'rudy-secret' }
        res = self.test_client.get('/api/v1/xapp_token', query_string=query)
        res_obj = json.loads(res.get_data())
        self.assertIn('xapp_token', res_obj)
        self.assertEqual(res_obj['xapp_token'], 'rudy-token')
        self.assertIn('expires_in', res_obj)
        # TODO assert res.expires_in is valid timestamp string

if __name__ == '__main__':
    unittest.main()
