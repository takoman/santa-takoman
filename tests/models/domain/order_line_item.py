# -*- coding: utf-8 -*-

import unittest
from mongoengine import *
from santa.models.domain import *
from tests import AppTestCase
from tests.factories import *

class OrderLineItemTests(AppTestCase):
    def setUp(self):
        super(OrderLineItemTests, self).setUp()
        self.order_line_item = OrderLineItemFactory.create()

    def test_required_properties(self):
        with self.assertRaisesRegexp(ValidationError, ".*Field is required: \['order'\].*"):
            OrderLineItem().save()

    def test_defined_properties(self):
        for p in ['type', 'custom_id', 'price', 'quantity', 'order', 'product',
                  'status', 'notes', 'created_at', 'updated_at']:
            self.assertTrue(hasattr(self.order_line_item, p))

    def test_allowed_type(self):
        for t in ['product', 'commission', 'shipping', 'tax', 'discount', 'coupon', 'fee']:
            try:
                self.order_line_item.type = t
                self.order_line_item.save()
            except ValidationError:
                self.fail("Saving type %s raises ValidationError unexpectedly", t)
        with self.assertRaisesRegexp(ValidationError, ".*Value must be one of \[.*\].*"):
            self.order_line_item.type = 'invalid_type'
            self.order_line_item.save()

    def test_allowed_status(self):
        for s in ['new', 'invoiced']:
            try:
                self.order_line_item.status = s
                self.order_line_item.save()
            except ValidationError:
                self.fail("Saving status %s raises ValidationError unexpectedly", s)
        with self.assertRaisesRegexp(ValidationError, ".*Value must be one of \[.*\].*"):
            self.order_line_item.status = 'invalid_status'
            self.order_line_item.save()

    def test_default_status(self):
        self.assertEqual(self.order_line_item.status, 'new')

    def test_optional_product_assoc(self):
        order_line_item = OrderLineItemFactory.create(product=None)
        self.assertIsNone(order_line_item.product)
        product = ProductFactory.create()
        order_line_item.product = product
        order_line_item.save()
        self.assertEqual(order_line_item.product, product)

    def test_update_order_total_signal_after_create_update(self):
        order = OrderFactory.create()
        item1 = OrderLineItemFactory.create(order=order, type='product', price=299, quantity=3)
        item2 = OrderLineItemFactory.create(order=order, type='coupon', price=-100, quantity=2)
        OrderLineItemFactory.create(order=order, type='commission', price=250, quantity=1)
        item1.price = 289
        item1.save()
        item2.quantity = 1
        item2.save()
        self.assertEqual(order.total, 289 * 3 + -100 + 250)

    def test_update_order_total_signal_after_delete(self):
        order = OrderFactory.create()
        OrderLineItemFactory.create(order=order, type='product', price=299, quantity=3)
        item = OrderLineItemFactory.create(order=order, type='coupon', price=-100, quantity=2)
        self.assertEqual(order.total, 299 * 3 + -100 * 2)
        item.delete()
        self.assertEqual(order.total, 299 * 3)

if __name__ == '__main__':
    unittest.main()
