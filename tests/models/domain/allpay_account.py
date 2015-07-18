# -*- coding: utf-8 -*-

import unittest
from tests import AppTestCase
from tests.factories import *
from mongoengine import *
from santa.models.domain import *

class AllPayAccountTests(AppTestCase):
    def setUp(self):
        super(AllPayAccountTests, self).setUp()
        self.allpay_account = AllPayAccountFactory.create()

    def test_required_properties(self):
        with self.assertRaisesRegexp(ValidationError, ".*Field is required: \['customer'\].*"):
            AllPayAccount().save()
        with self.assertRaisesRegexp(ValidationError, ".*Field is required: \['customer'\].*"):
            AllPayAccount(provider='AllPay').save()

    def test_defined_properties(self):
        for p in ['external_id', 'provider', 'customer', 'merchant', 'updated_at', 'created_at']:
            self.assertTrue(hasattr(self.allpay_account, p))

    def test_allowed_providers(self):
        user = UserFactory.create()
        with self.assertRaisesRegexp(ValidationError, ".*Value must be one of \['AllPay'\].*"):
            AllPayAccount(provider='Stripe', customer=user).save()

    def test_default_provider(self):
        user = UserFactory.create()
        account = AllPayAccount(customer=user).save()
        self.assertEqual(account.customer, user)

if __name__ == '__main__':
    unittest.main()
