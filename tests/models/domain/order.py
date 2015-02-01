# -*- coding: utf-8 -*-

import unittest
from tests import AppTestCase
from mongoengine import *
from santa.models.domain import *

class OrderTests(AppTestCase):
    def setUp(self):
        super(OrderTests, self).setUp()
        self.customer = User(name='buyer', email='buyer@gmail.com').save()
        self.merchant_user = User(name='seller', email='seller@gmail.com').save()
        self.merchant = Merchant(user=self.merchant_user, merchant_name='My Shop').save()
        Order(customer=self.customer, merchant=self.merchant).save()
        self.order = Order.objects.first()

    def test_required_properties(self):
        with self.assertRaisesRegexp(ValidationError, ".*Field is required: \['customer', 'merchant'\].*"):
            Order().save()
        with self.assertRaisesRegexp(ValidationError, ".*Field is required: \['merchant'\].*"):
            Order(customer=self.customer).save()
        with self.assertRaisesRegexp(ValidationError, ".*Field is required: \['customer'\].*"):
            Order(merchant=self.merchant).save()
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.merchant, self.merchant)

    def test_defined_properties(self):
        for p in ['customer', 'merchant', 'status', 'line_items', 'currency_source',
                  'currency_target', 'exchange_rate', 'notes', 'created_at', 'updated_at']:
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
        order_line_items.append(OrderLineItem(
            order=self.order, type='product', price=299, quantity=3).save())
        order_line_items.append(OrderLineItem(
            order=self.order, type='coupon', price=-100, quantity=2).save())
        order_line_items.append(OrderLineItem(
            order=self.order, type='commission', price=250, quantity=1).save())
        self.order.line_items = order_line_items
        self.assertEqual(self.order.calculate_total(), 299 * 3 + -100 * 2 + 250)

    def test_update_total_signal(self):
        order_line_items = []
        order_line_items.append(OrderLineItem(
            order=self.order, type='product', price=299, quantity=3).save())
        order_line_items.append(OrderLineItem(
            order=self.order, type='coupon', price=-100, quantity=2).save())
        order_line_items.append(OrderLineItem(
            order=self.order, type='commission', price=250, quantity=1).save())
        self.order.line_items = order_line_items
        self.order.save()
        self.assertEqual(self.order.total, 299 * 3 + -100 * 2 + 250)

if __name__ == '__main__':
    unittest.main()
