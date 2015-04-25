# -*- coding: utf-8 -*-

import unittest, datetime, json
from tests import AppTestCase
from mongoengine import *
from santa.models.domain import *
from santa.lib.common import me_to_json

class Image(EmbeddedDocument):
    image_url = URLField()

class Hero(Document):
    name = StringField()
    friends = ListField(ReferenceField('self'))
    images = ListField(EmbeddedDocumentField(Image))
    created_at = DateTimeField(default=datetime.datetime.now)

class MeToJsonTests(AppTestCase):
    def setUp(self):
        super(MeToJsonTests, self).setUp()
        time = datetime.datetime(2000, 1, 1, 0, 0)
        self.iron_man = Hero(name='Iron Man', images=[Image(image_url='http://iron.man')], created_at=time).save()
        self.super_man = Hero(name='Super Man', images=[Image(image_url='http://super.man')], created_at=time).save()
        self.spider_man = Hero(name='Spider Man', images=[Image(image_url='http://spider.man')], created_at=time).save()
        self.bat_man = Hero(name='Bat Man', images=[Image(image_url='http://bat.man')], created_at=time).save()
        self.iron_man.friends = [self.super_man, self.spider_man]
        self.iron_man.save()
        self.super_man.friends = [self.bat_man]
        self.super_man.save()
        self.spider_man.friends = [self.iron_man, self.super_man, self.bat_man]
        self.spider_man.save()
        self.maxDiff = None

    def test_document_to_json(self):
        iron_man = Hero.objects(name='Iron Man').first()
        self.assertDictEqual(json.loads(me_to_json(iron_man)), json.loads(json.dumps(
            {
                '_id': str(self.iron_man.id),
                'name': 'Iron Man',
                'images': [{ 'image_url': 'http://iron.man' }],
                'created_at': 'Sat, 01 Jan 2000 00:00:00 GMT',
                'friends': [
                    {
                        '_id': str(self.super_man.id),
                        'name': 'Super Man',
                        'images': [{ 'image_url': 'http://super.man' }],
                        'created_at': 'Sat, 01 Jan 2000 00:00:00 GMT',
                        'friends': [str(self.bat_man.id)]
                    },
                    {
                        '_id': str(self.spider_man.id),
                        'name': 'Spider Man',
                        'images': [{ 'image_url': 'http://spider.man' }],
                        'created_at': 'Sat, 01 Jan 2000 00:00:00 GMT',
                        'friends': [str(self.iron_man.id), str(self.super_man.id), str(self.bat_man.id)]
                    }
                ]
            }
        )))

    def test_query_set_to_json(self):
        qs = Hero.objects(name='Iron Man')
        self.assertListEqual(json.loads(me_to_json(qs)), json.loads(json.dumps(
            [{
                '_id': str(self.iron_man.id),
                'name': 'Iron Man',
                'images': [{ 'image_url': 'http://iron.man' }],
                'created_at': 'Sat, 01 Jan 2000 00:00:00 GMT',
                'friends': [
                    {
                        '_id': str(self.super_man.id),
                        'name': 'Super Man',
                        'images': [{ 'image_url': 'http://super.man' }],
                        'created_at': 'Sat, 01 Jan 2000 00:00:00 GMT',
                        'friends': [str(self.bat_man.id)]
                    },
                    {
                        '_id': str(self.spider_man.id),
                        'name': 'Spider Man',
                        'images': [{ 'image_url': 'http://spider.man' }],
                        'created_at': 'Sat, 01 Jan 2000 00:00:00 GMT',
                        'friends': [str(self.iron_man.id), str(self.super_man.id), str(self.bat_man.id)]
                    }
                ]
            }]
        )))

    def test_list_to_json(self):
        iron_man = Hero.objects(name='Iron Man').first()
        self.assertListEqual(json.loads(me_to_json([iron_man])), json.loads(json.dumps(
            [{
                '_id': str(self.iron_man.id),
                'name': 'Iron Man',
                'images': [{ 'image_url': 'http://iron.man' }],
                'created_at': 'Sat, 01 Jan 2000 00:00:00 GMT',
                'friends': [
                    {
                        '_id': str(self.super_man.id),
                        'friends': [str(self.bat_man.id)],
                        'name': 'Super Man',
                        'images': [{ 'image_url': 'http://super.man' }],
                        'created_at': 'Sat, 01 Jan 2000 00:00:00 GMT'
                    },
                    {
                        '_id': str(self.spider_man.id),
                        'friends': [str(self.iron_man.id), str(self.super_man.id), str(self.bat_man.id)],
                        'name': 'Spider Man',
                        'images': [{ 'image_url': 'http://spider.man' }],
                        'created_at': 'Sat, 01 Jan 2000 00:00:00 GMT'
                    }
                ]
            }]
        )))

if __name__ == '__main__':
    unittest.main()
