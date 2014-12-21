# -*- coding: utf-8 -*-
"""
    tests.api
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    api tests module
"""
from tests import AppTestCase
import unittest

class ApiTests(AppTestCase):

    def _request(self, verb, *args, **kwargs):
        with self.test_client as c:
            return getattr(c, verb)(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self._request('get', *args, **kwargs)

    def head(self, *args, **kwargs):
        return self._request('head', *args, **kwargs)

    def options(self, *args, **kwargs):
        return self._request('options', *args, **kwargs)

    def iter_responses(self, path, verbs=['get', 'head', 'options'], **kwargs):
        with self.test_client as c:
            for verb in verbs:
                yield getattr(c, verb.lower())(path, **kwargs)

    # Steal from Flask-Cors tests
    # https://github.com/wcdolphin/flask-cors/blob/e14122e918bcf5ffb41bfeab73c7094e3a18e471/tests/base_test.py#L73-L84
    def preflight(self, path, method='GET', json=True):
        headers = {'Access-Control-Request-Method': method}
        if json:
            headers.update({'Content-Type': 'application/json'})

        return self.options(path, headers=headers)

    def test_cors_allow_headers(self):
        res = self.preflight('/api/v1/xapp_token')
        self.assertEqual(res.headers.get('Access-Control-Allow-Headers'), 'Content-Type, X-XAPP-TOKEN')

    def test_cors_origin(self):
        for resp in self.iter_responses('/api/v1/xapp_token'):
            self.assertEqual(resp.headers.get('Access-Control-Allow-Origin'), '*')

if __name__ == '__main__':
    unittest.main()
