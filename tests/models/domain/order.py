# -*- coding: utf-8 -*-

import unittest
from mongoengine import *
from santa.models.domain import *
from tests import AppTestCase
from tests.factories import *

class OrderTests(AppTestCase):
    def setUp(self):
        super(OrderTests, self).setUp()
        self.order = OrderFactory.create()

    def test_required_properties(self):
        with self.assertRaisesRegexp(ValidationError, ".*Field is required: \['merchant'\].*"):
            Order().save()

    def test_defined_properties(self):
        for p in ['customer', 'merchant', 'status', 'shipping_address', 'order_line_items',
                  'currency_source', 'currency_target', 'exchange_rate', 'notes', 'access_key',
                  'created_at', 'updated_at']:
            self.assertTrue(hasattr(self.order, p))

    def test_allowed_status(self):
        for s in ['new', 'invoiced', 'paid', 'merchant_purchased', 'merchant_received',
                  'international_shipped', 'domestic_shipped', 'delivered', 'closed',
                  'canceled', 'refunded']:
            try:
                self.order.status = s
                self.order.save()
            except ValidationError:
                self.fail("Saving status %s raises ValidationError unexpectedly", s)
        with self.assertRaisesRegexp(ValidationError, ".*Value must be one of \[.*\].*"):
            self.order.status = 'invalid_status'
            self.order.save()

    def test_default_status(self):
        self.assertEqual(self.order.status, 'new')

    def test_allowed_currency(self):
        from santa.models.domain.order import SUPPORTED_CURRENCIES
        for c in SUPPORTED_CURRENCIES:
            try:
                self.order.currency_source = c
                self.order.currency_target = c
                self.order.save()
            except ValidationError:
                self.fail("Saving currency %s raises VlidationError unexpectedly", c)
        with self.assertRaisesRegexp(ValidationError, ".*Value must be one of \[.*\].*"):
            self.order.currency_source = 'UNSUPPORTED_CURRENCY'
            self.order.save()
        with self.assertRaisesRegexp(ValidationError, ".*Value must be one of \[.*\].*"):
            self.order.currency_target = 'UNSUPPORTED_CURRENCY'
            self.order.save()

    def test_default_currency_target(self):
        self.assertEqual(self.order.currency_target, 'TWD')

    def test_calculate_total(self):
        order_line_items = []
        order_line_items.append(OrderLineItemFactory.create(
            order=self.order, type='product', price=299, quantity=3))
        order_line_items.append(OrderLineItemFactory.create(
            order=self.order, type='coupon', price=-100, quantity=2))
        order_line_items.append(OrderLineItemFactory.create(
            order=self.order, type='commission', price=250, quantity=1))
        self.order.order_line_items = order_line_items
        self.assertEqual(self.order.calculate_total(), 299 * 3 + -100 * 2 + 250)

    def test_update_total_signal(self):
        order_line_items = []
        order_line_items.append(OrderLineItemFactory.create(
            order=self.order, type='product', price=299, quantity=3))
        order_line_items.append(OrderLineItemFactory.create(
            order=self.order, type='coupon', price=-100, quantity=2))
        order_line_items.append(OrderLineItemFactory.create(
            order=self.order, type='commission', price=250, quantity=1))
        self.order.order_line_items = order_line_items
        self.order.save()
        self.assertEqual(self.order.total, 299 * 3 + -100 * 2 + 250)

    def test_set_access_key_signal(self):
        order = OrderFactory.create()
        self.assertEqual(len(order.access_key), 48)
        access_key = order.access_key
        order.save()
        self.assertEqual(order.access_key, access_key)

if __name__ == '__main__':
    unittest.main()
