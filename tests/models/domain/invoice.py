# -*- coding: utf-8 -*-

import unittest
from mongoengine import *
from santa.models.domain import *
from tests import AppTestCase
from tests.factories import *

class InvoiceTests(AppTestCase):
    def setUp(self):
        super(InvoiceTests, self).setUp()
        self.invoice = InvoiceFactory.create()

    def test_required_properties(self):
        with self.assertRaisesRegexp(ValidationError, ".*Field is required: \['order'\].*"):
            Invoice().save()

    def test_defined_properties(self):
        for p in ['invoice_no', 'order', 'invoice_line_items', 'total', 'status',
                  'notes', 'due_at', 'created_at', 'updated_at']:
            self.assertTrue(hasattr(self.invoice, p))

    def test_allowed_status(self):
        for s in ['draft', 'unpaid', 'paid', 'overdue', 'void']:
            try:
                self.invoice.status = s
                self.invoice.save()
            except ValidationError:
                self.fail("Saving status %s raises ValidationError unexpectedly", s)
        with self.assertRaisesRegexp(ValidationError, ".*Value must be one of \[.*\].*"):
            self.invoice.status = 'invalid_status'
            self.invoice.save()

    def test_default_status(self):
        self.assertEqual(self.invoice.status, 'draft')

    def test_calculate_total(self):
        invoice_line_items = []
        invoice_line_items.append(InvoiceLineItemFactory.create(
            invoice=self.invoice, price=299, quantity=3))
        invoice_line_items.append(InvoiceLineItemFactory.create(
            invoice=self.invoice, price=-100, quantity=2))
        invoice_line_items.append(InvoiceLineItemFactory.create(
            invoice=self.invoice, price=250, quantity=1))
        self.invoice.invoice_line_items = invoice_line_items
        self.assertEqual(self.invoice.calculate_total(), 299 * 3 + -100 * 2 + 250)

    def test_update_total_signal(self):
        invoice_line_items = []
        invoice_line_items.append(InvoiceLineItemFactory.create(
            invoice=self.invoice, price=299, quantity=3))
        invoice_line_items.append(InvoiceLineItemFactory.create(
            invoice=self.invoice, price=-100, quantity=2))
        invoice_line_items.append(InvoiceLineItemFactory.create(
            invoice=self.invoice, price=250, quantity=1))
        self.invoice.invoice_line_items = invoice_line_items
        self.invoice.save()
        self.assertEqual(self.invoice.total, 299 * 3 + -100 * 2 + 250)

if __name__ == '__main__':
    unittest.main()
