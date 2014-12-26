# -*- coding: utf-8 -*-

import unittest
from tests import AppTestCase
from mongoengine import *
from santa.models.domain.user import User
from santa.models.domain.order import Order
from santa.models.domain.product import Product
from santa.models.domain.order_line_item import OrderLineItem

class OrderLineItemTests(AppTestCase):
    def setUp(self):
        super(OrderLineItemTests, self).setUp()
        customer = User(name='buyer', email='buyer@gmail.com').save()
        merchant = User(name='seller', email='seller@gmail.com').save()
        self.order = Order(customer=customer, merchant=merchant).save()
        OrderLineItem(order=self.order).save()
        self.order_line_item = OrderLineItem.objects.first()

    def test_required_properties(self):
        with self.assertRaisesRegexp(ValidationError, ".*Field is required: \['order'\].*"):
            OrderLineItem().save()

    def test_defined_properties(self):
        for p in ['type', 'custom_id', 'price', 'quantity', 'order', 'product',
                  'notes', 'created_at', 'updated_at']:
            self.assertTrue(hasattr(self.order_line_item, p))

    def test_allowed_type(self):
        for t in ['product', 'commission', 'shipping_dom_a', 'shipping_intl',
                  'shipping_dom_b', 'tax', 'discount', 'coupon', 'fee']:
            try:
                self.order_line_item.type = t
                self.order_line_item.save()
            except ValidationError:
                self.fail("Saving type %s raises ValidationError unexpectedly", s)
        with self.assertRaisesRegexp(ValidationError, ".*Value must be one of \[.*\].*"):
            self.order_line_item.type = 'invalid_type'
            self.order_line_item.save()

    def test_optional_product_assoc(self):
        self.assertIsNone(self.order_line_item.product)
        product = Product(title='iPhone').save()
        self.order_line_item.product = product
        self.order_line_item.save()
        order_line_item = OrderLineItem.objects.first()
        self.assertEqual(order_line_item.product, product)

    def test_update_order_total_signal(self):
        order_line_items = []
        order_line_items.append(OrderLineItem(
            order=self.order, type='product', price=299, quantity=3).save())
        order_line_items.append(OrderLineItem(
            order=self.order, type='coupon', price=-100, quantity=2).save())
        order_line_items.append(OrderLineItem(
            order=self.order, type='commission', price=250, quantity=1).save())
        self.order.line_items = order_line_items
        self.order.save()
        self.order.line_items[0].price = 289
        self.order.line_items[0].save()
        self.order.line_items[1].quantity = 1
        self.order.line_items[1].save()
        self.assertEqual(self.order.total, 289 * 3 + -100 + 250)

if __name__ == '__main__':
    unittest.main()
