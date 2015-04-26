# -*- coding: utf-8 -*-

from tests import AppTestCase
from tests.factories import *
from santa.models.domain import *
from santa.lib.common import me_to_json
from bson.objectid import ObjectId
import unittest, json

class ProductsEndpointsTests(AppTestCase):

    def setUp(self):
        super(ProductsEndpointsTests, self).setUp()
        self.product = ProductFactory.create(
            title=u'雙人牌Zwilling Henckels Pure 7 Piece Knife Block Set',
            brand=u'雙人牌',
            urls=['http://www.amazon.com/Zwilling-Henckels-Pure-Piece-Knife/dp/B005HVEGPW'],
            description=u'德國刀具舉世聞名，雖然差我們金門菜刀一點，但也是極品中的極品啦！這是眾所皆知的雙人牌，在台灣響當當的指甲剪，記得一把也要一兩千！現在刀組含架子正特價呢！原價20,000，現13000')

    #
    # GET /products
    #

    def test_public_access_products(self):
        res = self.test_client.get('/api/v1/products')
        self.assertEqual(res.status_code, 401)

    def test_rudy_access_products(self):
        res = self.test_client.get(
            '/api/v1/products', headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        products = json.loads(res.get_data())
        self.assertEqual(len(products), 1)
        expected = json.loads(me_to_json(Product.objects))
        self.assertListEqual(products, expected)

    #
    # GET /products/<product_id>
    #
    def test_get_certain_product(self):
        res = self.test_client.get(
            '/api/v1/products/' + str(self.product.id), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        product = json.loads(res.get_data())
        expected = json.loads(me_to_json(Product.objects(id=product['_id']).first()))
        self.assertDictEqual(product, expected)

    def test_get_product_by_invalid_object_id(self):
        res = self.test_client.get(
            '/api/v1/products/no-this-product', headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 400)
        self.assertIn("not a valid ObjectId", res.data)

    def test_get_non_existing_product(self):
        res = self.test_client.get(
            '/api/v1/products/' + str(ObjectId()), headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 404)
        self.assertIn("product not found", res.data)

    #
    # POST /products
    #
    def test_create_a_product(self):
        new_product_dict = {
            'title': u'Portmeirion精緻碗盤組',
            'brand': u'Portmeirion',
            'urls': ['https://tw.mall.yahoo.com/item/%E8%8B%B1%E5%9C%8BPortmeirion%E9%BB%9E%E5%BF%83-%E5%89%8D%E8%8F%9C-%E6%B2%BE%E9%86%AC%E7%A2%97%E7%9B%A4%E7%B5%84-%E6%A4%8D%E7%89%A9%E5%9C%92%E7%B3%BB%E5%88%97-p037855380911'],
            'description': u'男孩/女孩-刀叉組：Arthur : 800/組（含運）含: 1 x 盤子 (20cm), 1 x 碗(12cm) and 1 x 馬克杯.可使用於冷凍、烤箱、微波爐、洗碗機'
        }
        res = self.test_client.post('/api/v1/products',
                                    # Need to use string in the data param and
                                    # set content_type to json for parse_request
                                    # to successfully parse urls as an array.
                                    # http://werkzeug.pocoo.org/docs/0.9/test/#werkzeug.test.EnvironBuilder
                                    data=json.dumps(new_product_dict),
                                    content_type='application/json',
                                    headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 201)
        created_product = json.loads(res.get_data())
        expected = json.loads(me_to_json(Product.objects(id=created_product['_id']).first()))
        self.assertDictEqual(created_product, expected)

    #
    # PUT /products/<product_id>
    #
    def test_update_a_product(self):
        updated_product_dict = {
            'title': u'Portmeirion精緻碗盤組',
            'brand': u'Portmeirion',
            'urls': ['https://tw.mall.yahoo.com/item/%E8%8B%B1%E5%9C%8BPortmeirion%E9%BB%9E%E5%BF%83-%E5%89%8D%E8%8F%9C-%E6%B2%BE%E9%86%AC%E7%A2%97%E7%9B%A4%E7%B5%84-%E6%A4%8D%E7%89%A9%E5%9C%92%E7%B3%BB%E5%88%97-p037855380911'],
            'description': u'男孩/女孩-刀叉組：Arthur : 800/組（含運）含: 1 x 盤子 (20cm), 1 x 碗(12cm) and 1 x 馬克杯.可使用於冷凍、烤箱、微波爐、洗碗機'
        }
        res = self.test_client.get(
            '/api/v1/products', headers={'X-XAPP-TOKEN': self.client_app_token})
        product = json.loads(res.get_data())[0]

        res = self.test_client.put(
            'api/v1/products/' + product['_id'],
            data=json.dumps({
                'title': updated_product_dict['title'],
                'brand': updated_product_dict['brand'],
                'urls': updated_product_dict['urls'],
                'description': updated_product_dict['description']
            }),
            content_type='application/json',
            headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        updated_product = json.loads(res.get_data())
        expected = json.loads(me_to_json(Product.objects(id=updated_product['_id']).first()))
        self.assertDictEqual(updated_product, expected)

    #
    # DELETE /products/<product_id>
    #
    def test_delete_a_product(self):
        res = self.test_client.get(
            '/api/v1/products', headers={'X-XAPP-TOKEN': self.client_app_token})
        product = json.loads(res.get_data())[0]
        res = self.test_client.delete('api/v1/products/' + product['_id'],
                                      headers={'X-XAPP-TOKEN': self.client_app_token})
        self.assertEqual(res.status_code, 200)
        deleted_product = json.loads(res.get_data())
        self.assertDictEqual(product, deleted_product)
        self.assertEqual(len(Product.objects()), 0)

if __name__ == '__main__':
    unittest.main()
