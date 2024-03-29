# -*- coding: utf-8 -*-

from tests import AppTestCase
from tests.factories import *
from santa.models.domain import *
from santa.lib.common import me_to_json
from bson.objectid import ObjectId
import unittest, json

class InvoicePaymentsEndpointsTests(AppTestCase):

    def setUp(self):
        super(InvoicePaymentsEndpointsTests, self).setUp()
        self.invoice_payment = InvoicePaymentFactory.create()

    #
    # GET /invoice_payments
    #
    def test_public_access_invoice_payments(self):
        res = self.test_client.get('/api/v1/invoice_payments')
        self.assertEqual(res.status_code, 401)

    def test_rudy_access_invoice_payments(self):
        res = self.test_client.get(
            '/api/v1/invoice_payments', headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        invoice_payments = json.loads(res.get_data())
        self.assertEqual(len(invoice_payments), 1)

        expected = json.loads(me_to_json(InvoicePayment.objects))
        self.assertListEqual(invoice_payments, expected)

    def test_filter_invoice_payments_by_invoice_id(self):
        InvoicePaymentFactory.create()
        InvoicePaymentFactory.create()
        res = self.test_client.get(
            '/api/v1/invoice_payments', headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        invoice_payments = json.loads(res.get_data())
        self.assertEqual(len(invoice_payments), 3)
        res = self.test_client.get(
            '/api/v1/invoice_payments?invoice_id=' + str(self.invoice_payment.invoice.id), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        invoice_payments = json.loads(res.get_data())
        self.assertEqual(len(invoice_payments), 1)
        expected = json.loads(me_to_json(InvoicePayment.objects(invoice=str(self.invoice_payment.invoice.id))))
        self.assertListEqual(invoice_payments, expected)

    def test_filter_invoice_payments_by_external_id(self):
        InvoicePaymentFactory.create(external_id='123456')
        InvoicePaymentFactory.create()
        res = self.test_client.get(
            '/api/v1/invoice_payments', headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        invoice_payments = json.loads(res.get_data())
        self.assertEqual(len(invoice_payments), 3)
        res = self.test_client.get(
            '/api/v1/invoice_payments?external_id=123456', headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        invoice_payments = json.loads(res.get_data())
        self.assertEqual(len(invoice_payments), 1)
        expected = json.loads(me_to_json(InvoicePayment.objects(external_id='123456')))
        self.assertListEqual(invoice_payments, expected)

    #
    # GET /invoice_payments/<invoice_payment_id>
    #
    def test_get_certain_invoice_payment(self):
        res = self.test_client.get(
            '/api/v1/invoice_payments/' + str(self.invoice_payment.id), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        invoice_payment = json.loads(res.get_data())

        expected = json.loads(me_to_json(InvoicePayment.objects(id=invoice_payment['_id']).first()))
        self.assertDictEqual(invoice_payment, expected)

    def test_get_invoice_payment_by_invalid_object_id(self):
        res = self.test_client.get(
            '/api/v1/invoice_payments/no-this-invoice_payment', headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 400)
        self.assertIn("not a valid ObjectId", res.data)

    def test_get_non_existing_invoice_payment(self):
        res = self.test_client.get(
            '/api/v1/invoice_payments/' + str(ObjectId()), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("invoice payment not found", res.data)

    #
    # POST /invoice_payments
    #
    def test_create_an_invoice_payment(self):
        invoice = InvoiceFactory.create()
        allpay_account = AllPayAccountFactory.create()
        new_invoice_payment_dict = {
            'external_id': '1',
            'invoice': str(invoice.id),
            'payment_account': str(allpay_account.id),
            'total': 1000,
            'result': 'success',
            'message': u'交易非常的成功！啾咪！',
            'details': {
                'merchant_id': 'mid-1',
                'merchant_trade_no': 'mtn-1',
                'return_code': 1,
                'return_message': 'paid',
                'trade_no': 'tn-1',
                'trade_amount': 1000,
                'payment_date': '2012/03/20 13:04:29',
                'payment_type': 'ATM_TAISHIN',
                'payment_type_charge_fee': 25,
                'trade_date': '2012/03/16 12:03:12',
                'simulate_paid': 0,
                'raw': {
                    'merchant_id': 'mid-1',
                    'merchant_trade_no': 'mtn-1',
                    'return_code': 1,
                    'return_message': 'paid',
                    'trade_no': 'tn-1',
                    'trade_amount': 1000,
                    'payment_date': '2012/03/20 13:04:29',
                    'payment_type': 'ATM_TAISHIN',
                    'payment_type_charge_fee': 25,
                    'trade_date': '2012/03/16 12:03:12',
                    'simulate_paid': 0
                }
            },
            'allpay_offline_payment_details': {
                'merchant_id': 'mid-1',
                'merchant_trade_no': 'mtn-1',
                'return_code': 2,
                'return_message': 'Get VirtualAccount Succeed',
                'trade_no': 'tn-1',
                'trade_amount': 1000,
                'payment_type': 'ATM_TAISHIN',
                'trade_date': '2012/03/16 12:03:12',
                'expire_date': '2012/03/23 12:03:12',
                'bank_code': '812',
                'v_account': '9103522175887271',
                'raw': {
                    'merchant_id': 'mid-1',
                    'merchant_trade_no': 'mtn-1',
                    'return_code': 2,
                    'return_message': 'Get VirtualAccount Succeed',
                    'trade_no': 'tn-1',
                    'trade_amount': 1000,
                    'payment_type': 'ATM_TAISHIN',
                    'trade_date': '2012/03/16 12:03:12',
                    'expire_date': '2012/03/23 12:03:12',
                    'bank_code': '812',
                    'v_account': '9103522175887271'
                }
            }
        }
        res = self.test_client.post('/api/v1/invoice_payments',
                                    data=json.dumps(new_invoice_payment_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 201)
        created_invoice_payment = json.loads(res.get_data())

        expected = json.loads(me_to_json(InvoicePayment.objects(id=created_invoice_payment['_id']).first()))
        self.assertDictEqual(created_invoice_payment, expected)

    #
    # PUT /invoice_payments/<invoice_payment_id>
    #
    def test_update_an_invoice_payment(self):
        invoice = InvoiceFactory.create()
        allpay_account = AllPayAccountFactory.create()
        updated_invoice_payment_dict = {
            'external_id': '999',
            'invoice': str(invoice.id),
            'payment_account': str(allpay_account.id),
            'total': 300.99,
            'result': 'success',
            'message': u'史上最成功的交易！',
            'details': {
                'merchant_id': 'mid-199',
                'merchant_trade_no': 'mtn-168',
                'return_code': 1,
                'return_message': 'paid',
                'trade_no': 'tn-188',
                'trade_amount': 300.99,
                'payment_date': '2012/03/20 13:04:29',
                'payment_type': 'ATM_BOT',
                'payment_type_charge_fee': 25,
                'trade_date': '2012/03/16 12:03:12',
                'simulate_paid': 0,
                'raw': {
                    'merchant_id': 'mid-199',
                    'merchant_trade_no': 'mtn-168',
                    'return_code': 1,
                    'return_message': 'paid',
                    'trade_no': 'tn-188',
                    'trade_amount': 300.99,
                    'payment_date': '2012/03/20 13:04:29',
                    'payment_type': 'ATM_BOT',
                    'payment_type_charge_fee': 25,
                    'trade_date': '2012/03/16 12:03:12',
                    'simulate_paid': 0
                }
            },
            'allpay_offline_payment_details': {
                'merchant_id': 'mid-199',
                'merchant_trade_no': 'mtn-168',
                'return_code': 2,
                'return_message': 'Get VirtualAccount Succeed',
                'trade_no': 'tn-188',
                'trade_amount': 300.99,
                'payment_type': 'ATM_BOT',
                'trade_date': '2012/03/16 12:03:12',
                'expire_date': '2012/03/23 12:03:12',
                'bank_code': '813',
                'v_account': '8993522175997382',
                'raw': {
                    'merchant_id': 'mid-199',
                    'merchant_trade_no': 'mtn-168',
                    'return_code': 2,
                    'return_message': 'Get VirtualAccount Succeed',
                    'trade_no': 'tn-188',
                    'trade_amount': 300.99,
                    'payment_type': 'ATM_BOT',
                    'trade_date': '2012/03/16 12:03:12',
                    'expire_date': '2012/03/23 12:03:12',
                    'bank_code': '813',
                    'v_account': '8993522175997382'
                }
            }
        }
        res = self.test_client.put('/api/v1/invoice_payments/' + str(self.invoice_payment.id),
                                   data=json.dumps(updated_invoice_payment_dict),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        updated_invoice_payment = json.loads(res.get_data())
        self.assertEqual(len(InvoicePayment.objects), 1)
        expected = json.loads(me_to_json(InvoicePayment.objects(id=updated_invoice_payment['_id']).first()))
        self.assertDictEqual(updated_invoice_payment, expected)

    def test_update_a_non_existing_invoice_payment(self):
        res = self.test_client.put('/api/v1/invoice_payments/' + str(ObjectId()),
                                   data=json.dumps({}),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("invoice payment not found", res.data)

    #
    # DELETE /invoice_payments/<invoice_payment_id>
    #
    def test_delete_an_invoice_payment(self):
        res = self.test_client.get('/api/v1/invoice_payments/' + str(self.invoice_payment.id),
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        invoice_payment = json.loads(res.get_data())
        res = self.test_client.delete('api/v1/invoice_payments/' + str(self.invoice_payment.id),
                                      headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        deleted_invoice_payment = json.loads(res.get_data())
        self.assertDictEqual(invoice_payment, deleted_invoice_payment)
        self.assertEqual(len(InvoicePayment.objects()), 0)

    def test_delete_a_non_existing_invoice_payment(self):
        res = self.test_client.delete(
            '/api/v1/invoice_payments/' + str(ObjectId()), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("invoice payment not found", res.data)

if __name__ == '__main__':
    unittest.main()
