# -*- coding: utf-8 -*-

from tests import AppTestCase
from tests.factories import *
from santa.models.domain import *
from santa.lib.common import me_to_json
from bson.objectid import ObjectId
import unittest, json

class PaymentAccountsEndpointsTests(AppTestCase):

    def setUp(self):
        super(PaymentAccountsEndpointsTests, self).setUp()
        self.allpay_account = AllPayAccountFactory.create()

    #
    # GET /payment_accounts
    #
    def test_public_access_payment_accounts(self):
        res = self.test_client.get('/api/v1/payment_accounts')
        self.assertEqual(res.status_code, 401)

    def test_rudy_access_payment_accounts(self):
        res = self.test_client.get(
            '/api/v1/payment_accounts', headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        payment_accounts = json.loads(res.get_data())
        self.assertEqual(len(payment_accounts), 1)
        expected = json.loads(me_to_json(PaymentAccount.objects))
        self.assertListEqual(payment_accounts, expected)

    def test_filter_payment_accounts_by_customer_id(self):
        AllPayAccountFactory.create()
        AllPayAccountFactory.create()
        res = self.test_client.get(
            '/api/v1/payment_accounts', headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        payment_accounts = json.loads(res.get_data())
        self.assertEqual(len(payment_accounts), 3)

        res = self.test_client.get(
            '/api/v1/payment_accounts?customer_id=' + str(self.allpay_account.customer.id), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        payment_accounts = json.loads(res.get_data())
        self.assertEqual(len(payment_accounts), 1)
        expected = json.loads(me_to_json(PaymentAccount.objects(customer=str(self.allpay_account.customer.id))))
        self.assertListEqual(payment_accounts, expected)

    def test_filter_payment_accounts_by_merchant_id(self):
        AllPayAccountFactory.create()
        AllPayAccountFactory.create()
        res = self.test_client.get(
            '/api/v1/payment_accounts', headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        payment_accounts = json.loads(res.get_data())
        self.assertEqual(len(payment_accounts), 3)

        res = self.test_client.get(
            '/api/v1/payment_accounts?merchant_id=' + str(self.allpay_account.merchant.id), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        payment_accounts = json.loads(res.get_data())
        self.assertEqual(len(payment_accounts), 1)
        expected = json.loads(me_to_json(PaymentAccount.objects(merchant=str(self.allpay_account.merchant.id))))
        self.assertListEqual(payment_accounts, expected)

    #
    # GET /payment_accounts/<payment_account_id>
    #
    def test_get_certain_payment_account(self):
        res = self.test_client.get(
            '/api/v1/payment_accounts/' + str(self.allpay_account.id), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        allpay_account = json.loads(res.get_data())
        expected = json.loads(me_to_json(PaymentAccount.objects(id=allpay_account['_id']).first()))
        self.assertDictEqual(allpay_account, expected)

    def test_get_payment_account_by_invalid_object_id(self):
        res = self.test_client.get(
            '/api/v1/payment_accounts/no-this-payment_account', headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 400)
        self.assertIn("not a valid ObjectId", res.data)

    def test_get_non_existing_payment_account(self):
        res = self.test_client.get(
            '/api/v1/payment_accounts/' + str(ObjectId()), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("payment account not found", res.data)

    #
    # POST /payment_accounts
    #
    def test_create_an_payment_account(self):
        customer = UserFactory.create()
        new_payment_account_dict = {
            'external_id': 'id-0001',
            'provider': 'AllPay',
            'customer': str(customer.id)
        }
        res = self.test_client.post('/api/v1/payment_accounts',
                                    data=json.dumps(new_payment_account_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 201)
        created_payment_account = json.loads(res.get_data())
        expected = json.loads(me_to_json(PaymentAccount.objects(id=created_payment_account['_id']).first()))
        self.assertDictEqual(created_payment_account, expected)

    #
    # PUT /payment_accounts/<payment_account_id>
    #
    def test_update_an_payment_account(self):
        updated_customer = UserFactory.create()
        updated_payment_account_dict = {
            'external_id': 'id-0002',
            'customer': str(updated_customer.id)
        }
        res = self.test_client.put('/api/v1/payment_accounts/' + str(self.allpay_account.id),
                                   data=json.dumps(updated_payment_account_dict),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        updated_payment_account = json.loads(res.get_data())
        expected = json.loads(me_to_json(PaymentAccount.objects(id=updated_payment_account['_id']).first()))
        self.assertDictEqual(updated_payment_account, expected)

    def test_update_a_non_existing_payment_account(self):
        res = self.test_client.put('/api/v1/payment_accounts/' + str(ObjectId()),
                                   data=json.dumps({}),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("payment account not found", res.data)

    #
    # DELETE /payment_accounts/<payment_account_id>
    #
    def test_delete_an_payment_account(self):
        res = self.test_client.get('/api/v1/payment_accounts/' + str(self.allpay_account.id),
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        payment_account = json.loads(res.get_data())
        res = self.test_client.delete('api/v1/payment_accounts/' + str(self.allpay_account.id),
                                      headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        deleted_payment_account = json.loads(res.get_data())
        self.assertDictEqual(payment_account, deleted_payment_account)
        self.assertEqual(len(PaymentAccount.objects()), 0)

    def test_delete_a_non_existing_payment_account(self):
        res = self.test_client.delete(
            '/api/v1/payment_accounts/' + str(ObjectId()), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("payment account not found", res.data)

if __name__ == '__main__':
    unittest.main()
