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
                  'notes', 'due_at', 'access_key', 'created_at', 'updated_at']:
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

    def test_create_invoice_line_items(self):
        order = OrderFactory.create()
        new_olis = [OrderLineItemFactory.create(order=order) for i in [1, 2, 3]]
        [OrderLineItemFactory.create(order=order, status='invoiced') for i in [1, 2]]
        self.assertEqual(len(InvoiceLineItem.objects), 0)
        invoice = Invoice(order=order).save()
        invoice.create_invoice_line_items()

        self.assertEqual(len(InvoiceLineItem.objects), 3)
        for index, ili in enumerate(InvoiceLineItem.objects):
            self.assertEqual(ili.order_line_item.id, new_olis[index].id)
            self.assertEqual(ili.invoice.id, invoice.id)
        for oli in new_olis:
            oli.reload()
            self.assertEqual(oli.status, 'invoiced')

    def test_create_invoice_and_line_items_from_order(self):
        order = OrderFactory.create()
        new_olis = [OrderLineItemFactory.create(order=order) for i in [1, 2, 3]]
        [OrderLineItemFactory.create(order=order, status='invoiced') for i in [1, 2]]

        attrs = {
            'order': OrderFactory.create(),   # will be overwritten
            'status': 'void',                 # will be overwritten
            'notes': u'請在三天內付款',       # will be preserved
            'invalid_key': 'random'           # will not error
        }
        invoice = Invoice.create_invoice_and_line_items_from_order(order, attrs)

        # test invoice
        self.assertEqual(Invoice.objects.order_by('-created_at')[0], invoice)
        self.assertEqual(invoice.status, 'unpaid')
        self.assertEqual(invoice.notes, attrs['notes'])
        self.assertEqual(len(invoice.access_key), 48)

        # test order
        self.assertEqual(invoice.order.status, 'invoiced')

        # test invoice line items and order line items
        self.assertEqual(len(InvoiceLineItem.objects), 3)
        for index, ili in enumerate(InvoiceLineItem.objects):
            self.assertEqual(ili.order_line_item.id, new_olis[index].id)
            self.assertEqual(ili.invoice.id, invoice.id)
        for oli in new_olis:
            oli.reload()
            self.assertEqual(oli.status, 'invoiced')

    def test_set_access_key_signal(self):
        invoice = InvoiceFactory.create()
        self.assertEqual(len(invoice.access_key), 48)
        access_key = invoice.access_key
        invoice.save()
        self.assertEqual(invoice.access_key, access_key)

if __name__ == '__main__':
    unittest.main()
