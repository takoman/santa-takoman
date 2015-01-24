# -*- coding: utf-8 -*-

import unittest
from tests import AppTestCase
from mongoengine import *
from santa.models.domain import *

class MerchantTests(AppTestCase):
    def setUp(self):
        super(MerchantTests, self).setUp()
        self.user = User(name='seller', email='seller@gmail.com').save()
        Merchant(user=self.user, merchant_name='翔の飛行屋美國代買、美國代購').save()
        self.merchant = Merchant.objects.first()

    def test_required_properties(self):
        with self.assertRaisesRegexp(ValidationError, ".*Field is required: \['user', 'merchant_name'\].*"):
            Merchant().save()
        self.assertEqual(self.merchant.user, self.user)

    def test_defined_properties(self):
        for p in ['user', 'source_countries', 'updated_at', 'created_at']:
            self.assertTrue(hasattr(self.merchant, p))

    def test_allowed_countries(self):
        from santa.models.domain.merchant import SUPPORTED_COUNTRIES
        for c in SUPPORTED_COUNTRIES:
            try:
                self.merchant.cource_countries = [c]
                self.merchant.save()
            except ValidationError:
                self.fail("Saving source_countries [%c] raises ValidationError unexpectedly", c)
        with self.assertRaisesRegexp(ValidationError, ".*Value must be one of \[.*\].*"):
            self.merchant.source_countries = ['QQ']
            self.merchant.save()

if __name__ == '__main__':
    unittest.main()
