# -*- coding: utf-8 -*-
"""
    tests.api.client_apps_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    api client_apps tests module
"""
from pymongo import MongoClient
from tests import TestBase
import unittest, json

class ClientAppsTests(TestBase):

  def test_access_public_xapp_token(self):
    res = self.test_client.get('/xapp_token')
    assert res.status_code == 200

  def test_get_xapp_token(self):
    query = { 'client_id': 'rudy-test', 'client_secret': 'rudy-secret' }
    res = self.test_client.get('/xapp_token', query_string=query)
    res_obj = json.loads(res.get_data())
    assert 'xapp_token' in res_obj
    assert res_obj['xapp_token'] == 'rudy-token'
    assert 'expires_in' in res_obj
    # TODO assert res.expires_in is valid timestamp string

if __name__ == '__main__':
  unittest.main()
