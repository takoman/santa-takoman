# -*- coding: utf-8 -*-

from tests import AppTestCase
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
        product1 = Product(title=u'雙人牌7 Piece Knife Block Set').save()
        product2 = Product(title=u'海賊王漫畫全集（附海報）').save()
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
                                   headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 404)
        self.assertIn("missing order_id param", res.data)

    def test_rudy_access_order_line_items_with_non_existing_order(self):
        res = self.test_client.get('/api/v1/order_line_items?order_id=' + str(ObjectId()),
                                   headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order not found", res.data)

    def test_rudy_access_order_line_items_with_order(self):
        res = self.test_client.get('/api/v1/order_line_items?order_id=' + str(self.order.id),
                                   headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 200)
        items = json.loads(res.get_data())
        self.assertEqual(len(items), 4)
        for i, item_dict in enumerate(self.items_dict):
            self.assertDictContainsSubset(item_dict, items[i])

    #
    # GET /order_line_items/<order_line_item_id>
    #
    def test_get_certain_order_line_item(self):
        pass

    def test_get_certain_order_line_item_with_non_existing_id(self):
        pass

    #
    # POST /order_line_items
    #
    def test_add_line_item_without_an_order(self):
        pass

    def test_add_line_item_to_a_non_existing_order(self):
        pass

    def test_add_line_item_to_an_order(self):
        pass

    #
    # PUT /order_line_items/<order_line_item_id>
    #
    def test_update_a_non_existing_order_line_item(self):
        pass

    def test_update_an_order_line_item(self):
        pass

    #
    # DELETE /order_line_items/<order_line_item_id>
    #
    def test_delete_an_order_line_item(self):
        pass

    def test_delete_a_non_existing_order_line_item(self):
        pass

if __name__ == '__main__':
    unittest.main()
