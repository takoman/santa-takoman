# -*- coding: utf-8 -*-

import unittest
from tests import AppTestCase
from mongoengine import *
from santa.models.domain import *
from tests.factories import *

class InvoiceLineItemTests(AppTestCase):
    def setUp(self):
        super(InvoiceLineItemTests, self).setUp()
        self.invoice = InvoiceFactory.create()
        self.invoice_line_item = InvoiceLineItemFactory.create(invoice=self.invoice)
        self.invoice.invoice_line_items.append(self.invoice_line_item)
        self.invoice.save()
        self.order_line_item = self.invoice_line_item.order_line_item

    def test_required_properties(self):
        with self.assertRaisesRegexp(ValidationError, ".*Field is required: \['order_line_item', 'invoice'\].*"):
            InvoiceLineItem().save()

    def test_defined_properties(self):
        for p in ['invoice', 'order_line_item', 'price', 'quantity', 'notes',
                  'created_at', 'updated_at']:
            self.assertTrue(hasattr(self.invoice_line_item, p))

    def test_update_invoice_total_signal_after_updated(self):
        invoice = InvoiceFactory.create()
        item1 = InvoiceLineItemFactory.create(invoice=invoice, price=299, quantity=3)
        item2 = InvoiceLineItemFactory.create(invoice=invoice, price=-100, quantity=2)
        self.assertEqual(invoice.total, 299 * 3 + -100 * 2)
        item1.price = 289
        item1.save()
        item2.quantity = 1
        item2.save()
        self.assertEqual(invoice.total, 289 * 3 + -100)

    def test_update_invoice_total_signal_after_delete(self):
        invoice = InvoiceFactory.create()
        item1 = InvoiceLineItemFactory.create(invoice=invoice, price=299, quantity=3)
        item2 = InvoiceLineItemFactory.create(invoice=invoice, price=-100, quantity=2)
        self.assertEqual(invoice.total, 299 * 3 + -100 * 2)
        item1.price = 289
        item1.save()
        item2.delete()
        self.assertEqual(invoice.total, 289 * 3)

if __name__ == '__main__':
    unittest.main()
