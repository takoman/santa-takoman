# -*- coding: utf-8 -*-

from tests import AppTestCase
from tests.factories import *
from santa.models.domain import *
from santa.lib.common import me_to_json
from bson.objectid import ObjectId
import unittest, json

class OrdersEndpointsTests(AppTestCase):

    def setUp(self):
        super(OrdersEndpointsTests, self).setUp()
        self.order = OrderFactory.create()
        self.customer = self.order.customer
        self.merchant = self.order.merchant
        self.seller = self.merchant.user

    #
    # GET /orders
    #
    def test_public_access_orders(self):
        res = self.test_client.get('/api/v1/orders')
        self.assertEqual(res.status_code, 401)

    def test_rudy_access_orders(self):
        res = self.test_client.get(
            '/api/v1/orders', headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        orders = json.loads(res.get_data())
        self.assertEqual(len(orders), 1)

        expected = json.loads(me_to_json(Order.objects))
        self.assertListEqual(orders, expected)

    #
    # GET /orders/<order_id>
    #
    def test_get_certain_order(self):
        res = self.test_client.get(
            '/api/v1/orders/' + str(self.order.id), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        order = json.loads(res.get_data())
        expected = json.loads(me_to_json(Order.objects(id=order['_id']).first()))
        self.assertDictEqual(order, expected)

    def test_get_order_by_invalid_object_id(self):
        res = self.test_client.get(
            '/api/v1/orders/no-this-order', headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 400)
        self.assertIn("not a valid ObjectId", res.data)

    def test_get_non_existing_order(self):
        res = self.test_client.get(
            '/api/v1/orders/' + str(ObjectId()), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order not found", res.data)

    #
    # POST /orders
    #
    def test_create_an_order(self):
        merchant = MerchantFactory.create()
        customer = UserFactory.create()
        new_order_dict = {
            'customer': str(customer.id),
            'merchant': str(merchant.id),
            'currency_source': 'USD',
            'exchange_rate': 30,
            'notes': u'附上簽名照乙張'
        }
        res = self.test_client.post('/api/v1/orders',
                                    data=json.dumps(new_order_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 201)
        created_order = json.loads(res.get_data())
        expected = json.loads(me_to_json(Order.objects(id=created_order['_id']).first()))
        self.assertDictEqual(created_order, expected)

    #
    # PUT /orders/<order_id>
    #
    def test_update_an_order(self):
        updated_customer = UserFactory.create()
        updated_merchant = MerchantFactory.create()
        updated_order_dict = {
            'customer': str(updated_customer.id),
            'merchant': str(updated_merchant.id),
            'currency_source': 'GBP',
            'exchange_rate': 40.00,
            'notes': u'機車要加大鎖喔！！(((o(*ﾟ▽ﾟ*)o)))'
        }
        res = self.test_client.put('/api/v1/orders/' + str(self.order.id),
                                   data=json.dumps(updated_order_dict),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        updated_order = json.loads(res.get_data())
        expected = json.loads(me_to_json(Order.objects(id=updated_order['_id']).first()))
        self.assertDictEqual(updated_order, expected)

    def test_update_a_non_existing_order(self):
        res = self.test_client.put('/api/v1/orders/' + str(ObjectId()),
                                   data=json.dumps({}),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order not found", res.data)

    #
    # DELETE /orders/<order_id>
    #
    def test_delete_an_order(self):
        res = self.test_client.get('/api/v1/orders/' + str(self.order.id),
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        order = json.loads(res.get_data())
        res = self.test_client.delete('api/v1/orders/' + str(self.order.id),
                                      headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        deleted_order = json.loads(res.get_data())
        self.assertDictEqual(order, deleted_order)
        self.assertEqual(len(Order.objects()), 0)

    def test_delete_a_non_existing_order(self):
        res = self.test_client.delete(
            '/api/v1/orders/' + str(ObjectId()), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order not found", res.data)

if __name__ == '__main__':
    unittest.main()
