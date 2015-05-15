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
                  'notes', 'created_at', 'updated_at']:
            self.assertTrue(hasattr(self.order_line_item, p))

    def test_allowed_type(self):
        for t in ['product', 'commission', 'shipping', 'tax', 'discount', 'coupon', 'fee']:
            try:
                self.order_line_item.type = t
                self.order_line_item.save()
            except ValidationError:
                self.fail("Saving type %s raises ValidationError unexpectedly", s)
        with self.assertRaisesRegexp(ValidationError, ".*Value must be one of \[.*\].*"):
            self.order_line_item.type = 'invalid_type'
            self.order_line_item.save()

    def test_optional_product_assoc(self):
        order_line_item = OrderLineItemFactory.create(product=None)
        self.assertIsNone(order_line_item.product)
        product = ProductFactory.create()
        order_line_item.product = product
        order_line_item.save()
        self.assertEqual(order_line_item.product, product)

    def test_update_order_total_signal(self):
        order = OrderFactory.create()
        order_line_items = []
        order_line_items.append(OrderLineItemFactory(
            order=order, type='product', price=299, quantity=3))
        order_line_items.append(OrderLineItemFactory(
            order=order, type='coupon', price=-100, quantity=2))
        order_line_items.append(OrderLineItemFactory(
            order=order, type='commission', price=250, quantity=1))
        order.order_line_items = order_line_items
        order.save()
        order.order_line_items[0].price = 289
        order.order_line_items[0].save()
        order.order_line_items[1].quantity = 1
        order.order_line_items[1].save()
        self.assertEqual(order.total, 289 * 3 + -100 + 250)

if __name__ == '__main__':
    unittest.main()
