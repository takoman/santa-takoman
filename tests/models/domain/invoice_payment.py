# -*- coding: utf-8 -*-

import unittest
from mongoengine import *
from santa.models.domain import *
from santa.models.domain.invoice import INVOICE_STATUSES
from tests import AppTestCase
from tests.factories import *

class InvoicePaymentTests(AppTestCase):
    def setUp(self):
        super(InvoicePaymentTests, self).setUp()
        self.payment = InvoicePaymentFactory.create()

    def test_required_properties(self):
        with self.assertRaisesRegexp(ValidationError, ".*Field is required: \['external_id'\].*"):
            InvoicePayment().save()

    def test_defined_properties(self):
        for p in ['external_id', 'invoice', 'payment_account', 'total', 'result', 'message', 'details',
                  'allpay_offline_payment_details', 'created_at', 'updated_at']:
            self.assertTrue(hasattr(self.payment, p))

    def test_allowed_result(self):
        for s in ['success', 'failure']:
            try:
                self.payment.result = s
                self.payment.save()
            except ValidationError:
                self.fail("Saving status %s raises ValidationError unexpectedly", s)
        with self.assertRaisesRegexp(ValidationError, ".*Value must be one of \[.*\].*"):
            self.payment.result = 'invalid_result'
            self.payment.save()

    def test_payment_and_offline_payment_details(self):
        payment = InvoicePayment(
            external_id='9998',
            details=AllPayPaymentDetails(
                merchant_id='007',
                merchant_trade_no='123456789'),
            allpay_offline_payment_details=AllPayOfflinePaymentDetails(
                payment_type='ATM_TAISHIN',
                bank_code='812',
                v_account='9103522175887271')
        )
        payment.save()
        p = InvoicePayment.objects(external_id='9998').first()
        self.assertEqual(p.details.merchant_id, '007')
        self.assertEqual(p.details.merchant_trade_no, '123456789')
        self.assertEqual(p.allpay_offline_payment_details.payment_type, 'ATM_TAISHIN')
        self.assertEqual(p.allpay_offline_payment_details.bank_code, '812')
        self.assertEqual(p.allpay_offline_payment_details.v_account, '9103522175887271')

    def test_update_unpaid_invoice_status_signal(self):
        for s in ['unpaid']:
            self.payment.invoice.status = s
            self.payment.invoice.save()
            self.payment.result = u'success'
            self.payment.save()
            self.assertEqual(self.payment.invoice.status, u'paid')

    def test_not_update_other_invoice_status_signal(self):
        other_statuses = [x for x in INVOICE_STATUSES if x not in ['unpaid']]
        for s in other_statuses:
            self.payment.invoice.status = s
            self.payment.invoice.save()
            self.payment.result = u'success'
            self.payment.save()
            self.assertEqual(self.payment.invoice.status, s)

if __name__ == '__main__':
    unittest.main()
