# -*- coding: utf-8 -*-

from tests import AppTestCase
from tests.factories import *
from santa.models.domain import *
from santa.lib.common import me_to_json
from santa.lib.util import date_to_str
from bson.objectid import ObjectId
from dateutil import parser
import unittest, json

class OrderPaymentsEndpointsTests(AppTestCase):

    def setUp(self):
        super(OrderPaymentsEndpointsTests, self).setUp()
        self.order_payment = OrderPaymentFactory.create()

    #
    # GET /order_payments
    #
    def test_public_access_order_payments(self):
        res = self.test_client.get('/api/v1/order_payments')
        self.assertEqual(res.status_code, 401)

    def test_rudy_access_order_payments(self):
        res = self.test_client.get(
            '/api/v1/order_payments', headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 200)
        order_payments = json.loads(res.get_data())
        self.assertEqual(len(order_payments), 1)

        self.assertDictContainsSubset(
            json.loads(me_to_json(self.order_payment)),
            order_payments[0]
        )

    #
    # GET /order_payments/<order_payment_id>
    #
    def test_get_certain_order_payment(self):
        res = self.test_client.get(
            '/api/v1/order_payments/' + str(self.order_payment.id), headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 200)
        order_payment = json.loads(res.get_data())
        self.assertDictContainsSubset(
            json.loads(me_to_json(self.order_payment)),
            order_payment
        )

    def test_get_order_payment_by_invalid_object_id(self):
        res = self.test_client.get(
            '/api/v1/order_payments/no-this-order_payment', headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 400)
        self.assertIn("not a valid ObjectId", res.data)

    def test_get_non_existing_order_payment(self):
        res = self.test_client.get(
            '/api/v1/order_payments/' + str(ObjectId()), headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order payment not found", res.data)

    #
    # POST /order_payments
    #
    def test_create_an_order_payment(self):
        order = OrderFactory.create()
        allpay_account = AllPayAccountFactory.create()
        new_order_payment_dict = {
            'external_id': '1',
            'order': str(order.id),
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
                'offline_payment_details': {
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
        res = self.test_client.post('/api/v1/order_payments',
                                    data=json.dumps(new_order_payment_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 201)
        created_order_payment = json.loads(res.get_data())

        # The API converts the timestamps to RFC 1123 format, so we have to
        # manually convert them here for the assertion.
        # https://github.com/takoman/santa/blob/ec0bf9d63e9a92ffeda78405629449323f06c738/santa/lib/common.py#L18

        # We may register new methods for equality check of timestamps.
        # https://docs.python.org/2/library/unittest.html#unittest.TestCase.assertDictContainsSubset
        new_order_payment_dict['details']['payment_date'] = date_to_str(
            parser.parse(new_order_payment_dict['details']['payment_date']))
        new_order_payment_dict['details']['trade_date'] = date_to_str(
            parser.parse(new_order_payment_dict['details']['trade_date']))
        new_order_payment_dict['details']['offline_payment_details']['trade_date'] = date_to_str(
            parser.parse(new_order_payment_dict['details']['offline_payment_details']['trade_date']))
        new_order_payment_dict['details']['offline_payment_details']['expire_date'] = date_to_str(
            parser.parse(new_order_payment_dict['details']['offline_payment_details']['expire_date']))
        self.assertDictContainsSubset(new_order_payment_dict, created_order_payment)

    #
    # PUT /order_payments/<order_payment_id>
    #
    def test_update_an_order_payment(self):
        order = OrderFactory.create()
        allpay_account = AllPayAccountFactory.create()
        updated_order_payment_dict = {
            'external_id': '999',
            'order': str(order.id),
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
                'offline_payment_details': {
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
        res = self.test_client.put('/api/v1/order_payments/' + str(self.order_payment.id),
                                   data=json.dumps(updated_order_payment_dict),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 200)
        updated_order_payment = json.loads(res.get_data())
        self.assertEqual(len(OrderPayment.objects), 1)
        self.assertEqual(str(self.order_payment.id), updated_order_payment['_id'])

        # The API converts the timestamps to RFC 1123 format, so we have to
        # manually convert them here for the assertion.
        # https://github.com/takoman/santa/blob/ec0bf9d63e9a92ffeda78405629449323f06c738/santa/lib/common.py#L18

        # We may register new methods for equality check of timestamps.
        # https://docs.python.org/2/library/unittest.html#unittest.TestCase.assertDictContainsSubset
        updated_order_payment_dict['details']['payment_date'] = date_to_str(
            parser.parse(updated_order_payment_dict['details']['payment_date']))
        updated_order_payment_dict['details']['trade_date'] = date_to_str(
            parser.parse(updated_order_payment_dict['details']['trade_date']))
        updated_order_payment_dict['details']['offline_payment_details']['trade_date'] = date_to_str(
            parser.parse(updated_order_payment_dict['details']['offline_payment_details']['trade_date']))
        updated_order_payment_dict['details']['offline_payment_details']['expire_date'] = date_to_str(
            parser.parse(updated_order_payment_dict['details']['offline_payment_details']['expire_date']))
        self.assertDictContainsSubset(updated_order_payment_dict, updated_order_payment)

    def test_update_a_non_existing_order_payment(self):
        res = self.test_client.put('/api/v1/order_payments/' + str(ObjectId()),
                                   data=json.dumps({}),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order payment not found", res.data)

    #
    # DELETE /order_payments/<order_payment_id>
    #
    def test_delete_an_order_payment(self):
        res = self.test_client.get('/api/v1/order_payments/' + str(self.order_payment.id),
                                   headers={'X-XAPP-TOKEN': 'rudy-token'})
        order_payment = json.loads(res.get_data())
        res = self.test_client.delete('api/v1/order_payments/' + str(self.order_payment.id),
                                      headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 200)
        deleted_order_payment = json.loads(res.get_data())
        self.assertDictEqual(order_payment, deleted_order_payment)
        self.assertEqual(len(OrderPayment.objects()), 0)

    def test_delete_a_non_existing_order_payment(self):
        res = self.test_client.delete(
            '/api/v1/order_payments/' + str(ObjectId()), headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order payment not found", res.data)

if __name__ == '__main__':
    unittest.main()
