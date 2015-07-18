# -*- coding: utf-8 -*-

import unittest, json, datetime
from mongoengine import *
from santa.models.domain import *
from santa.models.mixins.updated_at_mixin import UpdatedAtMixin
from santa.lib.common import me_to_json
from tests import AppTestCase

class Order(UpdatedAtMixin, Document):
    shipping_address = EmbeddedDocumentField(Location)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

class LocationTests(AppTestCase):
    def setUp(self):
        super(LocationTests, self).setUp()

    def test_english_locations(self):
        location = {
            'address': '50 Christopher Columbus Dr.',
            'address_2': 'Apt. 3209',
            'city': 'Jersey City',
            'region': 'NJ',
            'zipcode': '07302',
            'country': 'US'
        }
        order = Order(shipping_address=Location(**location)).save()
        self.assertDictContainsSubset(location, json.loads(me_to_json(order))['shipping_address'])

    def test_unicode_locations(self):
        location = {
            'address': u'吉林路 26 巷 38 號 2 樓之 2',
            'district': u'中山區',
            'city': u'台北市',
            'zipcode': '10457',
            'country': 'TW'
        }
        order = Order(shipping_address=Location(**location)).save()
        self.assertDictContainsSubset(location, json.loads(me_to_json(order))['shipping_address'])

    @unittest.skip("Need to serialize the PointField better.")
    def test_locations_coordinates(self):
        location = {
            'address': '50 Christopher Columbus Dr.',
            'address_2': 'Apt. 3209',
            'city': 'Jersey City',
            'region': 'NJ',
            'zipcode': '07302',
            'coordinates': [40.7188845, -74.0395288],
            'country': 'US'
        }
        order = Order(shipping_address=Location(**location)).save()
        self.assertDictContainsSubset(location, json.loads(me_to_json(order))['shipping_address'])

if __name__ == '__main__':
    unittest.main()
