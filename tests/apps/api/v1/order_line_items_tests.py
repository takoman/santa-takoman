# -*- coding: utf-8 -*-

from tests import AppTestCase
from tests.factories import *
from santa.models.domain import *
from bson.objectid import ObjectId
import unittest, json

class OrderLineItemsEndpointsTests(AppTestCase):

    def setUp(self):
        super(OrderLineItemsEndpointsTests, self).setUp()
        buyer = User(name='Buyer B.', email='buyer@takoman.co', password='password').save()
        seller = User(name='Seller S.', email='seller@takoman.co', password='password').save()
        merchant = Merchant(user=seller, merchant_name=u'翔の飛行屋美國、日本代買代購').save()
        self.order = Order(customer=buyer, merchant=merchant).save()
        product1 = ProductFactory.create()
        product2 = ProductFactory.create()
        self.items_dict = [
            {
                'type': 'product',
                'price': 399.50,
                'quantity': 1,
                'order': str(self.order.id),
                'product': str(product1.id)
            },
            {
                'type': 'product',
                'price': 23.99,
                'quantity': 2,
                'order': str(self.order.id),
                'product': str(product2.id)
            },
            {
                'type': 'commission',
                'price': 50,
                'quantity': 1,
                'order': str(self.order.id),
            },
            {
                'type': 'discount',
                'price': 25.50,
                'quantity': 1,
                'order': str(self.order.id)
            },
        ]
        self.items = [OrderLineItem(**i).save() for i in self.items_dict]
        self.order.line_items = self.items
        self.order.save()

    #
    # GET /order_line_items
    #
    def test_public_access_order_line_items(self):
        res = self.test_client.get('/api/v1/order_line_items')
        self.assertEqual(res.status_code, 401)

    def test_rudy_access_order_line_items_without_order(self):
        res = self.test_client.get('/api/v1/order_line_items',
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("missing order id", res.data)

    def test_rudy_access_order_line_items_with_non_existing_order(self):
        res = self.test_client.get('/api/v1/order_line_items?order_id=' + str(ObjectId()),
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order not found", res.data)

    def test_rudy_access_order_line_items_with_order(self):
        res = self.test_client.get('/api/v1/order_line_items?order_id=' + str(self.order.id),
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        items = json.loads(res.get_data())
        self.assertEqual(len(items), 4)
        for i, item_dict in enumerate(self.items_dict):
            self.assertDictContainsSubset(item_dict, items[i])

    #
    # GET /order_line_items/<order_line_item_id>
    #
    def test_get_certain_order_line_item(self):
        for i, item in enumerate(self.items):
            res = self.test_client.get(
                '/api/v1/order_line_items/' + str(item.id), headers={'X-XAPP-TOKEN': self.client_app_token})
            self.assertEqual(res.status_code, 200)
            fetched_item = json.loads(res.get_data())
            self.assertDictContainsSubset(self.items_dict[i], fetched_item)

    def test_get_certain_order_line_item_with_non_existing_id(self):
        res = self.test_client.get(
            '/api/v1/order_line_items/' + str(ObjectId()), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order line item not found", res.data)

    #
    # POST /order_line_items
    #
    def test_add_line_item_without_an_order(self):
        product = Product(title=u'Coach Darcy 蝴蝶結長夾(黑色)').save()
        item_dict = {
            'type': 'product',
            'price': 399.50,
            'quantity': 1,
            'product': str(product.id)
        }
        res = self.test_client.post('/api/v1/order_line_items',
                                    data=json.dumps(item_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("missing order id", res.data)

    def test_add_line_item_to_a_non_existing_order(self):
        product = Product(title=u'Coach Darcy 蝴蝶結長夾(黑色)').save()
        item_dict = {
            'type': 'product',
            'price': 399.50,
            'quantity': 1,
            'order': str(ObjectId()),
            'product': str(product.id)
        }
        res = self.test_client.post('/api/v1/order_line_items',
                                    data=json.dumps(item_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order not found", res.data)

    def test_add_line_item_with_a_non_existing_product(self):
        item_dict = {
            'type': 'product',
            'price': 399.50,
            'quantity': 1,
            'order': str(self.order.id),
            'product': str(ObjectId())
        }
        res = self.test_client.post('/api/v1/order_line_items',
                                    data=json.dumps(item_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("product not found", res.data)

    def test_add_line_item_to_an_order(self):
        product = Product(title=u'Coach Darcy 蝴蝶結長夾(黑色)').save()
        item_dict = {
            'type': 'product',
            'price': 399.50,
            'quantity': 1,
            'order': str(self.order.id),
            'product': str(product.id)
        }
        res = self.test_client.post('/api/v1/order_line_items',
                                    data=json.dumps(item_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 201)
        created_item = json.loads(res.get_data())
        self.assertDictContainsSubset(item_dict, created_item)

    #
    # PUT /order_line_items/<order_line_item_id>
    #
    def test_update_a_non_existing_order_line_item(self):
        res = self.test_client.put('/api/v1/order_line_items/' + str(ObjectId()),
                                   data=json.dumps({}),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order line item not found", res.data)

    def test_update_an_order_line_item(self):
        item = self.items[0]
        product = Product(title=u'2015 Coach Darcy 蝴蝶結長夾(黑色)').save()
        updated_item_dict = {
            'type': 'commission',
            'price': 50.50,
            'quantity': 2,
            'product': str(product.id)
        }
        res = self.test_client.put('/api/v1/order_line_items/' + str(item.id),
                                   data=json.dumps(updated_item_dict),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        updated_item = json.loads(res.get_data())
        self.assertDictContainsSubset(updated_item_dict, updated_item)

    #
    # DELETE /order_line_items/<order_line_item_id>
    #
    def test_delete_an_order_line_item(self):
        res = self.test_client.get('api/v1/order_line_items/' + str(self.items[0].id),
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        item = json.loads(res.get_data())
        res = self.test_client.delete('api/v1/order_line_items/' + str(self.items[0].id),
                                      headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        deleted_item = json.loads(res.get_data())
        self.assertDictEqual(item, deleted_item)
        self.assertEqual(len(OrderLineItem.objects()), 3)

    def test_delete_a_non_existing_order_line_item(self):
        res = self.test_client.delete('api/v1/order_line_items/' + str(ObjectId()),
                                      headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order line item not found", res.data)

if __name__ == '__main__':
    unittest.main()
