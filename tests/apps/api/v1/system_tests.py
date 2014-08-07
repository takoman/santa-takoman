import unittest
from nose2.tools import such
from tests import AppLifeCycle
import json

with such.A('System endpoint') as it:
    it.uses(AppLifeCycle)

    with it.having('GET /system/up'):
        with it.having('system up'):
            @it.should('return system up info')
            def test_get_system_up(case):
                res = case.test_client.get('/api/v1/system/up')
                it.assertEquals(res.status_code, 200)
                it.assertEquals(json.loads(res.get_data()), {'flask': True, 'database': True})

        with it.having('database down'):
            @it.should('return database down info')
            @unittest.skip("Need a way to shutdown/start database during tests.")
            def test_get_database_down(case):
                pass

it.createTests(globals())
