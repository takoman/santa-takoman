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
        invoice_line_items = []
        invoice_line_items.append(InvoiceLineItemFactory.create(
            invoice=invoice, price=299, quantity=3))
        invoice_line_items.append(InvoiceLineItemFactory.create(
            invoice=invoice, price=-100, quantity=2))
        invoice.invoice_line_items = invoice_line_items
        invoice.save()
        self.assertEqual(len(invoice.invoice_line_items), 2)
        self.assertEqual(invoice.total, 299 * 3 + -100 * 2)
        invoice.invoice_line_items[0].price = 289
        invoice.invoice_line_items[0].save()
        invoice.invoice_line_items[1].quantity = 1
        invoice.invoice_line_items[1].save()
        self.assertEqual(len(invoice.invoice_line_items), 2)
        self.assertEqual(invoice.total, 289 * 3 + -100)

if __name__ == '__main__':
    unittest.main()
