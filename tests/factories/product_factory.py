# -*- coding: utf-8 -*-

import factory
from santa.models.domain import *
from factory.mongoengine import MongoEngineFactory
from . import *

__all__ = ('ProductFactory',)

class ProductFactory(MongoEngineFactory):
    class Meta:
        model = Product

    title = factory.Sequence(lambda n: '星巴克城市紀念杯 {0}'.format(n))
    seller_product_id = factory.Sequence(lambda n: 'seller-product-id-{0}'.format(n))
    brand = u'星巴克'
    color = u'彩色'
    size = u'無'
    # images = [factory.SubFactory(ImageFactory)]
    urls = ['http://starbucks.com/mug/1', 'http://starbucks.com/mug/1/details']
    description = u'星巴克全新 2015 城市紀念杯限定版，不買可惜！'
    notes = u'買三送一，要買要快！'
