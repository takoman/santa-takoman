# -*- coding: utf-8 -*-

from tests import AppTestCase
from tests.factories import *
from santa.models.domain import *
from bson.objectid import ObjectId
from santa.lib.common import me_to_json
import unittest, json

class InvoiceLineItemsEndpointsTests(AppTestCase):

    def setUp(self):
        super(InvoiceLineItemsEndpointsTests, self).setUp()
        order = OrderFactory.create()
        product1 = ProductFactory.create()
        product2 = ProductFactory.create()
        order_line_items_dict = [
            {
                'type': 'product',
                'price': 399.50,
                'quantity': 1,
                'order': str(order.id),
                'product': str(product1.id)
            },
            {
                'type': 'product',
                'price': 23.99,
                'quantity': 2,
                'order': str(order.id),
                'product': str(product2.id)
            },
            {
                'type': 'commission',
                'price': 50,
                'quantity': 1,
                'order': str(order.id),
            },
            {
                'type': 'discount',
                'price': 25.50,
                'quantity': 1,
                'order': str(order.id)
            },
        ]
        [OrderLineItemFactory.create(**i) for i in order_line_items_dict]
        self.invoice = InvoiceFactory.create(order=order)

    #
    # GET /invoice_line_items
    #
    def test_public_access_invoice_line_items(self):
        res = self.test_client.get('/api/v1/invoice_line_items')
        self.assertEqual(res.status_code, 401)

    def test_rudy_access_invoice_line_items_without_invoice(self):
        res = self.test_client.get('/api/v1/invoice_line_items',
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("missing invoice id", res.data)

    def test_rudy_access_invoice_line_items_with_non_existing_invoice(self):
        res = self.test_client.get('/api/v1/invoice_line_items?invoice_id=' + str(ObjectId()),
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("invoice not found", res.data)

    def test_rudy_access_invoice_line_items_with_invoice(self):
        res = self.test_client.get('/api/v1/invoice_line_items?invoice_id=' + str(self.invoice.id),
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        response_items = json.loads(res.get_data())
        self.assertEqual(len(response_items), 4)
        invoice_line_items = InvoiceLineItem.objects(invoice=self.invoice)
        self.assertListEqual(response_items, json.loads(me_to_json(invoice_line_items)))

    #
    # GET /invoice_line_items/<invoice_line_item_id>
    #
    def test_get_certain_invoice_line_item(self):
        invoice_line_items = InvoiceLineItem.objects(invoice=self.invoice)
        for i, item in enumerate(invoice_line_items):
            res = self.test_client.get(
                '/api/v1/invoice_line_items/' + str(item.id), headers={'X-XAPP-TOKEN': self.client_app_token})
            self.assertEqual(res.status_code, 200)
            fetched_item = json.loads(res.get_data())
            self.assertDictEqual(fetched_item, json.loads(me_to_json(item)))

    def test_get_certain_invoice_line_item_with_non_existing_id(self):
        res = self.test_client.get(
            '/api/v1/invoice_line_items/' + str(ObjectId()), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("invoice line item not found", res.data)

    #
    # POST /invoice_line_items
    #
    def test_add_line_item_without_an_invoice(self):
        item_dict = {
            'price': 399.50,
            'quantity': 1
        }
        res = self.test_client.post('/api/v1/invoice_line_items',
                                    data=json.dumps(item_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("missing invoice id", res.data)

    def test_add_line_item_to_a_non_existing_invoice(self):
        item_dict = {
            'price': 399.50,
            'quantity': 1,
            'invoice': str(ObjectId())
        }
        res = self.test_client.post('/api/v1/invoice_line_items',
                                    data=json.dumps(item_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("invoice not found", res.data)

    def test_add_line_item_without_an_order_line_item(self):
        item_dict = {
            'price': 399.50,
            'quantity': 1,
            'invoice': str(self.invoice.id)
        }
        res = self.test_client.post('/api/v1/invoice_line_items',
                                    data=json.dumps(item_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("missing order line item id", res.data)

    def test_add_line_item_with_a_non_existing_order_line_item(self):
        item_dict = {
            'price': 399.50,
            'quantity': 1,
            'invoice': str(self.invoice.id),
            'order_line_item': str(ObjectId())
        }
        res = self.test_client.post('/api/v1/invoice_line_items',
                                    data=json.dumps(item_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("order line item not found", res.data)

    def test_add_line_item_to_an_invoice_with_different_orders(self):
        order_line_item = OrderLineItemFactory.create()
        item_dict = {
            'price': 399.50,
            'quantity': 1,
            'invoice': str(self.invoice.id),
            'order_line_item': str(order_line_item.id)
        }
        res = self.test_client.post('/api/v1/invoice_line_items',
                                    data=json.dumps(item_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 400)
        self.assertIn("order line item and invoice associated with different order", res.data)

    def test_add_line_item_to_an_invoice(self):
        order_line_item = OrderLineItemFactory.create(order=self.invoice.order)
        item_dict = {
            'price': 399.50,
            'quantity': 1,
            'invoice': str(self.invoice.id),
            'order_line_item': str(order_line_item.id)
        }
        res = self.test_client.post('/api/v1/invoice_line_items',
                                    data=json.dumps(item_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 201)
        created_item = json.loads(res.get_data())
        expected = InvoiceLineItem.objects(id=created_item['_id']).first()
        self.assertDictEqual(created_item, json.loads(me_to_json(expected)))

        # The invoice should have 1 more invoice line items.
        res = self.test_client.get('/api/v1/invoice_line_items?invoice_id=' + str(self.invoice.id),
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        response_items = json.loads(res.get_data())
        self.assertEqual(len(response_items), 5)

    #
    # PUT /invoice_line_items/<invoice_line_item_id>
    #
    def test_update_a_non_existing_invoice_line_item(self):
        res = self.test_client.put('/api/v1/invoice_line_items/' + str(ObjectId()),
                                   data=json.dumps({}),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("invoice line item not found", res.data)

    def test_update_an_invoice_line_item(self):
        invoice_line_items = InvoiceLineItem.objects(invoice=self.invoice)
        invoice_line_item = invoice_line_items[0]
        invoice = InvoiceFactory.create()
        order_line_item = OrderLineItemFactory.create()
        updated_item_dict = {
            'price': 50.50,
            'quantity': 2,
            'invoice': str(invoice.id),
            'order_line_item': str(order_line_item.id)
        }
        res = self.test_client.put('/api/v1/invoice_line_items/' + str(invoice_line_item.id),
                                   data=json.dumps(updated_item_dict),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        updated_item = json.loads(res.get_data())
        expected = InvoiceLineItem.objects(id=updated_item['_id']).first()
        self.assertDictContainsSubset(updated_item, json.loads(me_to_json(expected)))

    #
    # DELETE /invoice_line_items/<invoice_line_item_id>
    #
    def test_delete_an_invoice_line_item(self):
        invoice_line_items = InvoiceLineItem.objects(invoice=self.invoice)
        res = self.test_client.get('api/v1/invoice_line_items/' + str(invoice_line_items[0].id),
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        item = json.loads(res.get_data())
        res = self.test_client.delete('api/v1/invoice_line_items/' + str(invoice_line_items[0].id),
                                      headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        deleted_item = json.loads(res.get_data())
        self.assertDictEqual(item, deleted_item)
        self.assertEqual(len(InvoiceLineItem.objects()), 3)

    def test_delete_a_non_existing_invoice_line_item(self):
        res = self.test_client.delete('api/v1/invoice_line_items/' + str(ObjectId()),
                                      headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("invoice line item not found", res.data)

if __name__ == '__main__':
    unittest.main()
