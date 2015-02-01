# -*- coding: utf-8 -*-

from tests import AppTestCase
from santa.models.domain import *
from bson.objectid import ObjectId
import unittest, json

class OrdersEndpointsTests(AppTestCase):

    def setUp(self):
        super(OrdersEndpointsTests, self).setUp()
        self.buyer = User(name='Buyer B.', email='buyer@takoman.co', password='password').save()
        self.seller = User(name='Seller S.', email='seller@takoman.co', password='password').save()
        self.merchant = Merchant(user=self.seller, merchant_name=u'翔の飛行屋美國、日本代買代購').save()
        self.order = Order(customer=self.buyer, merchant=self.merchant).save()

    #
    # GET /orders
    #
    def test_public_access_merchants(self):
        res = self.test_client.get('/api/v1/orders')
        self.assertEqual(res.status_code, 401)

    def test_rudy_access_products(self):
        res = self.test_client.get(
            '/api/v1/orders', headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 200)
        orders = json.loads(res.get_data())
        self.assertEqual(len(orders), 1)

        self.assertDictContainsSubset({
            '_id': str(self.order.id),
            'customer': str(self.buyer.id),
            'merchant': str(self.merchant.id),
        }, orders[0])

    #
    # GET /orders/<order_id>
    #
    def test_get_certain_order(self):
        res = self.test_client.get(
            '/api/v1/orders/' + str(self.order.id), headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 200)
        order = json.loads(res.get_data())
        self.assertDictContainsSubset({
            '_id': str(self.order.id),
            'customer': str(self.buyer.id),
            'merchant': str(self.merchant.id)
        }, order)

    def test_get_order_by_invalid_object_id(self):
        res = self.test_client.get(
            '/api/v1/orders/no-this-order', headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 400)
        self.assertIn("not a valid ObjectId", res.data)

    def test_get_non_existing_order(self):
        res = self.test_client.get(
            '/api/v1/orders/' + str(ObjectId()), headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order not found", res.data)

    #
    # POST /orders
    #
    def test_create_an_order(self):
        buyer = User(name='Iron Man', email='ironman@takoman.co', password='password').save()
        seller = User(name='Cat Woman', email='catwoman@takoman.co', password='password').save()
        merchant = Merchant(user=seller, merchant_name=u'貓女の機車專賣').save()
        new_order_dict = {
            'customer': str(buyer.id),
            'merchant': str(merchant.id),
            'currency_source': 'USD',
            'exchange_rate': 30,
            'notes': u'附上簽名照乙張'
        }
        res = self.test_client.post('/api/v1/orders',
                                    data=json.dumps(new_order_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 201)
        created_order = json.loads(res.get_data())
        self.assertDictContainsSubset(new_order_dict, created_order)

    #
    # PUT /orders/<order_id>
    #
    def test_update_an_order(self):
        updated_buyer = User(name='Super Man', email='superman@takoman.co', password='password').save()
        updated_seller = User(name='Super Woman', email='superwoman@takoman.co', password='password').save()
        updated_merchant = Merchant(user=updated_seller, merchant_name=u'女超人の機車專賣').save()
        updated_order_dict = {
            'customer': str(updated_buyer.id),
            'merchant': str(updated_merchant.id),
            'currency_source': 'GBP',
            'exchange_rate': 40.00,
            'notes': u'機車要加大鎖喔！！(((o(*ﾟ▽ﾟ*)o)))'
        }
        res = self.test_client.put('/api/v1/orders/' + str(self.order.id),
                                   data=json.dumps(updated_order_dict),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 200)
        updated_order = json.loads(res.get_data())
        self.assertDictContainsSubset(updated_order_dict, updated_order)

    def test_update_a_non_existing_order(self):
        res = self.test_client.put('/api/v1/orders/' + str(ObjectId()),
                                   data=json.dumps({}),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order not found", res.data)

    #
    # DELETE /orders/<order_id>
    #
    def test_delete_an_order(self):
        res = self.test_client.get('/api/v1/orders/' + str(self.order.id),
                                   headers={'X-XAPP-TOKEN': 'rudy-token'})
        order = json.loads(res.get_data())
        res = self.test_client.delete('api/v1/orders/' + str(self.order.id),
                                      headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 200)
        deleted_order = json.loads(res.get_data())
        self.assertDictEqual(order, deleted_order)
        self.assertEqual(len(Order.objects()), 0)

    def test_delete_a_non_existing_order(self):
        res = self.test_client.delete(
            '/api/v1/orders/' + str(ObjectId()), headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order not found", res.data)

if __name__ == '__main__':
    unittest.main()
