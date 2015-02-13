# -*- coding: utf-8 -*-

import unittest
from tests import AppTestCase
from mongoengine import *
from santa.models.domain import *
from santa.models.domain.order import ORDER_STATUSES

class OrderPaymentTests(AppTestCase):
    def setUp(self):
        super(OrderPaymentTests, self).setUp()
        self.customer = User(name='buyer', email='buyer@gmail.com').save()
        self.merchant = User(name='seller', email='seller@gmail.com').save()
        self.order = Order(customer=self.customer, merchant=self.merchant).save()
        OrderPayment(external_id='0001', order=self.order).save()
        self.payment = OrderPayment.objects.first()

    def test_required_properties(self):
        with self.assertRaisesRegexp(ValidationError, ".*Field is required: \['external_id'\].*"):
            OrderPayment().save()
        self.assertEqual(self.payment.external_id, '0001')
        self.assertEqual(self.payment.order, self.order)

    def test_defined_properties(self):
        for p in ['external_id', 'order', 'payment_account', 'total', 'result', 'message', 'details',
                  'created_at', 'updated_at']:
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
        payment = OrderPayment(
            external_id='9998',
            details=AllPayPaymentDetails(
                merchant_id='007',
                merchant_trade_no='123456789',
                offline_payment_details=AllPayOfflinePaymentDetails(
                    payment_type='ATM_TAISHIN',
                    bank_code='812',
                    v_account='9103522175887271'
                )
            )
        )
        payment.save()
        p = OrderPayment.objects(external_id='9998').first()
        self.assertEqual(p.details.merchant_id, '007')
        self.assertEqual(p.details.merchant_trade_no, '123456789')
        self.assertEqual(p.details.offline_payment_details.payment_type, 'ATM_TAISHIN')
        self.assertEqual(p.details.offline_payment_details.bank_code, '812')
        self.assertEqual(p.details.offline_payment_details.v_account, '9103522175887271')

    def test_update_new_or_invoiced_order_status_signal(self):
        for s in ['new', 'invoiced']:
            self.payment.order.status = s
            self.payment.order.save()
            self.payment.result = u'success'
            self.payment.save()
            self.assertEqual(self.payment.order.status, u'paid')

    def test_not_update_other_order_status_signal(self):
        other_statuses = [x for x in ORDER_STATUSES if x not in ['new', 'invoiced']]
        for s in other_statuses:
            self.payment.order.status = s
            self.payment.order.save()
            self.payment.result = u'success'
            self.payment.save()
            self.assertEqual(self.payment.order.status, s)

if __name__ == '__main__':
    unittest.main()
