# -*- coding: utf-8 -*-

import unittest, datetime
from santa.lib.util import str_to_date, date_to_str
from tests import AppTestCase

class StrToDateTests(AppTestCase):
    def test_convert_valid_iso_8601_string_to_date(self):
        string = '2015-01-01T00:00:00-04:00'
        date = str_to_date(string)
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, datetime.datetime(2015, 1, 1, 4, 0))

    def test_convert_empty_string_to_date(self):
        date = str_to_date('')
        self.assertIsNone(date)

class DateToStrTests(AppTestCase):
    def test_convert_valid_date_to_iso_8601_string(self):
        date = datetime.datetime(2015, 1, 1, 4, 0)
        string = date_to_str(date)
        self.assertEqual(string, '2015-01-01T04:00:00+00:00')

    def test_convert_empty_date_to_iso_8601_string(self):
        string = date_to_str('')
        self.assertIsNone(string)

if __name__ == '__main__':
    unittest.main()
