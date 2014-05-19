# -*- coding: utf-8 -*-
"""
    tests.api.client_apps_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    api client_apps tests module
"""
from pymongo import MongoClient
from santa import create_app
import unittest, json

class ClientAppsTests(unittest.TestCase):
  # before each
  def setUp(self):
    app = create_app()
    app.config['TESTING'] = True
    self.app = app.test_client()
    # Insert some fake data
    client = MongoClient(app.config['MONGO_HOST'], app.config['MONGO_PORT'])
    self.db = client[app.config['MONGO_DBNAME']]
    rudy_app = {
      'client_id'     : 'rudy-test',
      'client_secret' : 'rudy-secret',
      'token'         : 'rudy-token'
    }
    self.db.client_apps.insert(rudy_app)

  # after each
  def tearDown(self):
    # Remove the collection after each testcase
    self.db.client_apps.remove()

  def test_access_public_xapp_token(self):
    res = self.app.get('/xapp_token')
    assert res.status_code == 200

  def test_get_xapp_token(self):
    query = { 'client_id': 'rudy-test', 'client_secret': 'rudy-secret' }
    res = self.app.get('/xapp_token', query_string=query)
    res_obj = json.loads(res.get_data())
    assert 'xapp_token' in res_obj
    assert res_obj['xapp_token'] == 'rudy-token'
    assert 'expires_in' in res_obj
    # TODO assert res.expires_in is valid timestamp string

if __name__ == '__main__':
  unittest.main()
