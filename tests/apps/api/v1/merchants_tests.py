# -*- coding: utf-8 -*-

from tests import AppTestCase
from santa.models.domain import *
from bson.objectid import ObjectId
import unittest, json

class MerchantsEndpointsTests(AppTestCase):

    def setUp(self):
        super(MerchantsEndpointsTests, self).setUp()
        self.user = User(name='Clare Tai', email='clare@takoman.co', password='password').save()
        self.merchant = Merchant(user=self.user, merchant_name=u'翔の飛行屋美國、日本代買代購').save()

    #
    # GET /merchants
    #

    def test_public_access_merchants(self):
        res = self.test_client.get('/api/v1/merchants')
        self.assertEqual(res.status_code, 401)

    def test_rudy_access_products(self):
        res = self.test_client.get(
            '/api/v1/merchants', headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 200)
        merchants = json.loads(res.get_data())
        self.assertEqual(len(merchants), 1)

        # TODO: The user attributes should be embedded in the response;
        # not just the BSON ID.
        self.assertDictContainsSubset({
            '_id': str(self.merchant.id),
            'user': str(self.user.id),
            'merchant_name': u'翔の飛行屋美國、日本代買代購'
        }, merchants[0])

    #
    # GET /merchants/<merchant_id>
    #

    def test_get_certain_merchant(self):
        res = self.test_client.get(
            '/api/v1/merchants/' + str(self.merchant.id), headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 200)
        merchant = json.loads(res.get_data())
        self.assertDictContainsSubset({
            '_id': str(self.merchant.id),
            'user': str(self.user.id),
            'merchant_name': u'翔の飛行屋美國、日本代買代購'
        }, merchant)

    def test_get_not_valid_object_id_merchant(self):
        res = self.test_client.get(
            '/api/v1/merchants/no-this-merchant', headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 400)
        self.assertIn("not a valid ObjectId", res.data)

    def test_get_not_existing_merchant(self):
        res = self.test_client.get(
            '/api/v1/merchants/' + str(ObjectId()), headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 404)
        self.assertIn("merchant not found", res.data)

    #
    # POST /merchants
    #
    def test_create_a_merchant(self):
        new_merchant_dict = {
            'user': str(self.user.id),
            'merchant_name': u'翔の飛行屋美國、日本代買代購',
            'source_countries': ['US', 'TW']
        }
        res = self.test_client.post('/api/v1/merchants',
                                    data=json.dumps(new_merchant_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 201)
        created_merchant = json.loads(res.get_data())
        self.assertDictContainsSubset(new_merchant_dict, created_merchant)

    #
    # PUT /merchants/<merchant_id>
    #
    def test_update_a_merchat(self):
        updated_user = User(name='Iron Man', email='ironman@takoman.co', password='password').save()
        updated_merchant_dict = {
            'user': str(updated_user.id),
            'merchant_name': u'奈の飛行屋英國、日本代買代購',
            'source_countries': ['GB', 'JP']
        }
        res = self.test_client.put('/api/v1/merchants/' + str(self.merchant.id),
                                   data=json.dumps(updated_merchant_dict),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 200)
        created_merchant = json.loads(res.get_data())
        self.assertDictContainsSubset(updated_merchant_dict, created_merchant)

    def test_update_a_non_existing_merchant(self):
        res = self.test_client.put('/api/v1/merchants/' + str(ObjectId()),
                                   data=json.dumps({}),
                                   content_type='application/json',
                                   headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 404)
        self.assertIn("merchant not found", res.data)

    #
    # DELETE /merchants/<merchant_id>
    #
    def test_delete_a_merchant(self):
        res = self.test_client.get('/api/v1/merchants/' + str(self.merchant.id),
                                   headers={'X-XAPP-TOKEN': 'rudy-token'})
        merchant = json.loads(res.get_data())
        res = self.test_client.delete('api/v1/merchants/' + str(self.merchant.id),
                                      headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 200)
        deleted_merchant = json.loads(res.get_data())
        self.assertDictEqual(merchant, deleted_merchant)
        self.assertEqual(len(Merchant.objects()), 0)

    def test_delete_a_non_existing_merchant(self):
        res = self.test_client.delete(
            '/api/v1/merchants/' + str(ObjectId()), headers={'X-XAPP-TOKEN': 'rudy-token'})
        self.assertEqual(res.status_code, 404)
        self.assertIn("merchant not found", res.data)

    def test_delete_user_also_delete_merchant(self):
        pass

if __name__ == '__main__':
    unittest.main()
