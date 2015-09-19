# -*- coding: utf-8 -*-

from tests import AppTestCase
from tests.factories import *
from santa.models.domain import *
from santa.lib.util import date_to_str
from santa.lib.common import me_to_json
from bson.objectid import ObjectId
import unittest, json, datetime

class InvoicesEndpointsTests(AppTestCase):

    def setUp(self):
        super(InvoicesEndpointsTests, self).setUp()
        self.invoice = InvoiceFactory.create()

    #
    # GET /invoices
    #
    def test_public_access_merchants(self):
        res = self.test_client.get('/api/v1/invoices')
        self.assertEqual(res.status_code, 401)

    def test_rudy_access_products(self):
        res = self.test_client.get(
            '/api/v1/invoices', headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        invoices = json.loads(res.get_data())
        self.assertEqual(len(invoices), 1)

        expected = json.loads(me_to_json(Invoice.objects))
        self.assertListEqual(invoices, expected)

    #
    # GET /invoices/<invoice_id>
    #
    def test_get_certain_invoice_without_access_key(self):
        res = self.test_client.get(
            '/api/v1/invoices/' + str(self.invoice.id), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 400)
        self.assertIn("missing access key", res.data)

    def test_get_certain_invoice_with_wrong_access_key(self):
        url = '/api/v1/invoices/' + str(self.invoice.id) + '?access_key=wrong_access_key'
        res = self.test_client.get(url, headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("invoice not found", res.data)

    def test_get_certain_invoice(self):
        url = '/api/v1/invoices/' + str(self.invoice.id) + '?access_key=' + self.invoice.access_key
        res = self.test_client.get(url, headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        invoice = json.loads(res.get_data())
        expected = json.loads(me_to_json(Invoice.objects(id=invoice['_id']).first()))
        self.assertDictEqual(invoice, expected)

    def test_get_invoice_by_invalid_object_id(self):
        url = '/api/v1/invoices/no-this-invoice?access_key=' + self.invoice.access_key
        res = self.test_client.get(url, headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 400)
        self.assertIn("not a valid ObjectId", res.data)

    def test_get_non_existing_invoice(self):
        url = '/api/v1/invoices/' + str(ObjectId()) + '?access_key=' + self.invoice.access_key
        res = self.test_client.get(url, headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("invoice not found", res.data)

    #
    # POST /invoices
    #
    def test_create_an_invoice_with_non_existing_order(self):
        due_at = date_to_str(datetime.datetime.utcnow() + datetime.timedelta(days=21))
        new_invoice_dict = {
            'order': str(ObjectId()),
            'notes': u'附上簽名照乙張',
            'due_at': due_at
        }
        res = self.test_client.post('/api/v1/invoices',
                                    data=json.dumps(new_invoice_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 400)
        self.assertIn("order not exist", res.data)

    def test_create_an_invoice(self):
        order = OrderFactory.create()
        due_at = date_to_str(datetime.datetime.utcnow() + datetime.timedelta(days=21))
        new_invoice_dict = {
            'order': str(order.id),
            'notes': u'附上簽名照乙張',
            'due_at': due_at
        }
        res = self.test_client.post('/api/v1/invoices',
                                    data=json.dumps(new_invoice_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 201)
        created_invoice = json.loads(res.get_data())
        expected = json.loads(me_to_json(Invoice.objects(id=created_invoice['_id']).first()))
        self.assertDictEqual(created_invoice, expected)

    def test_create_an_invoice_with_access_key(self):
        order = OrderFactory.create()
        due_at = date_to_str(datetime.datetime.utcnow() + datetime.timedelta(days=21))
        new_invoice_dict = {
            'order': str(order.id),
            'access_key': '1 2 3 5'
        }
        res = self.test_client.post('/api/v1/invoices',
                                    data=json.dumps(new_invoice_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 201)
        created_invoice = json.loads(res.get_data())
        expected = json.loads(me_to_json(Invoice.objects(id=created_invoice['_id']).first()))
        self.assertDictEqual(created_invoice, expected)
        self.assertNotEqual(expected['access_key'], new_invoice_dict['access_key'])
        self.assertEqual(len(expected['access_key']), 48)

    def test_create_associated_invoice_line_items(self):
        order = OrderFactory.create()
        olis = [OrderLineItemFactory.create(order=order) for i in [1, 2, 3]]
        due_at = date_to_str(datetime.datetime.utcnow() + datetime.timedelta(days=21))
        new_invoice_dict = {
            'order': str(order.id),
            'notes': u'附上簽名照乙張',
            'due_at': due_at
        }
        self.assertEqual(len(InvoiceLineItem.objects), 0)
        res = self.test_client.post('/api/v1/invoices',
                                    data=json.dumps(new_invoice_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 201)
        created_invoice = json.loads(res.get_data())
        expected = json.loads(me_to_json(Invoice.objects(id=created_invoice['_id']).first()))
        self.assertDictEqual(created_invoice, expected)

        self.assertEqual(len(InvoiceLineItem.objects), 3)
        for index, ili in enumerate(InvoiceLineItem.objects):
            self.assertEqual(ili.order_line_item.id, olis[index].id)
            self.assertEqual(str(ili.invoice.id), created_invoice['_id'])
        for oli in olis:
            oli.reload()
            self.assertEqual(oli.status, 'invoiced')

    #
    # PUT /invoices/<invoice_id>
    #
    def test_update_an_invoice(self):
        order = OrderFactory.create()
        due_at = date_to_str(datetime.datetime.utcnow() + datetime.timedelta(days=28))
        updated_invoice_dict = {
            'order': str(order.id),
            'notes': u'機車要加大鎖喔！！(((o(*ﾟ▽ﾟ*)o)))',
            'due_at': due_at
        }
        res = self.test_client.put('/api/v1/invoices/' + str(self.invoice.id),
                                   data=json.dumps(updated_invoice_dict),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        updated_invoice = json.loads(res.get_data())
        expected = json.loads(me_to_json(Invoice.objects(id=updated_invoice['_id']).first()))
        self.assertDictEqual(updated_invoice, expected)

    def test_update_a_non_existing_invoice(self):
        res = self.test_client.put('/api/v1/invoices/' + str(ObjectId()),
                                   data=json.dumps({}),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("invoice not found", res.data)

    #
    # DELETE /invoices/<invoice_id>
    #
    def test_delete_an_invoice(self):
        url = '/api/v1/invoices/' + str(self.invoice.id) + '?access_key=' + self.invoice.access_key
        res = self.test_client.get(url, headers={'X-XAPP-TOKEN': self.client_app_token})
        invoice = json.loads(res.get_data())
        res = self.test_client.delete('api/v1/invoices/' + str(self.invoice.id),
                                      headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        deleted_invoice = json.loads(res.get_data())
        self.assertDictEqual(invoice, deleted_invoice)
        self.assertEqual(len(Invoice.objects()), 0)

    def test_delete_a_non_existing_invoice(self):
        res = self.test_client.delete(
            '/api/v1/invoices/' + str(ObjectId()), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("invoice not found", res.data)

if __name__ == '__main__':
    unittest.main()
