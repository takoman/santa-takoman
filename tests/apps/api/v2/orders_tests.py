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

        merchant_access = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='credentials',
            email=self.order.merchant.user.email,
            password='password'
        ))
        self.merchant_access_token = json.loads(merchant_access.data).get('access_token')
        customer_access = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='credentials',
            email=self.order.customer.email,
            password='password'
        ))
        self.customer_access_token = json.loads(customer_access.data).get('access_token')

    #
    # GET /orders/<order_id>
    #
    def test_get_certain_order_without_access_token(self):
        res = self.test_client.get(
            '/api/v2/orders/' + str(self.order.id), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 401)
        self.assertIn('please provide proper credentials', res.data)

    def test_get_certain_order_with_invalid_access_token(self):
        res = self.test_client.get(
            '/api/v2/orders/' + str(self.order.id), headers={'X-ACCESS-TOKEN': 'random-access-token-do-not-open'})
        self.assertEqual(res.status_code, 401)
        self.assertIn('please provide proper credentials', res.data)

    def test_get_certain_order_with_merchants_access_token(self):
        res = self.test_client.get(
            '/api/v2/orders/' + str(self.order.id), headers={'X-ACCESS-TOKEN': self.merchant_access_token})
        self.assertEqual(res.status_code, 200)
        order = json.loads(res.get_data())
        expected = json.loads(me_to_json(Order.objects(id=order['_id']).first()))
        self.assertDictEqual(order, expected)

    def test_get_certain_order_with_customers_access_token(self):
        res = self.test_client.get(
            '/api/v2/orders/' + str(self.order.id), headers={'X-ACCESS-TOKEN': self.customer_access_token})
        self.assertEqual(res.status_code, 200)
        order = json.loads(res.get_data())
        expected = json.loads(me_to_json(Order.objects(id=order['_id']).first()))
        self.assertDictEqual(order, expected)

    def test_get_certain_order_with_somebodyelses_access_token(self):
        user = UserFactory.create()
        user_access = self.test_client.post('/oauth2/access_token', data=dict(
            client_id=self.client_app.client_id,
            client_secret=self.client_app.client_secret,
            grant_type='credentials',
            email=user.email,
            password='password'
        ))
        access_token = json.loads(user_access.data).get('access_token')
        res = self.test_client.get(
            '/api/v2/orders/' + str(self.order.id), headers={'X-ACCESS-TOKEN': access_token})
        self.assertEqual(res.status_code, 400)
        self.assertIn('user not authorized to access the order', res.data)

    def test_get_certain_order(self):
        res = self.test_client.get(
            '/api/v2/orders/' + str(self.order.id), headers={'X-ACCESS-TOKEN': self.merchant_access_token})
        self.assertEqual(res.status_code, 200)
        order = json.loads(res.get_data())
        expected = json.loads(me_to_json(Order.objects(id=order['_id']).first()))
        self.assertDictEqual(order, expected)

    def test_get_order_by_invalid_object_id(self):
        res = self.test_client.get(
            '/api/v2/orders/no-this-order', headers={'X-ACCESS-TOKEN': self.merchant_access_token})
        self.assertEqual(res.status_code, 400)
        self.assertIn("not a valid ObjectId", res.data)

    def test_get_non_existing_order(self):
        res = self.test_client.get(
            '/api/v2/orders/' + str(ObjectId()), headers={'X-ACCESS-TOKEN': self.merchant_access_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order not found", res.data)

if __name__ == '__main__':
    unittest.main()
