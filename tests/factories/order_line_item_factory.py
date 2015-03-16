# -*- coding: utf-8 -*-

import factory
from santa.models.domain import *
from factory.mongoengine import MongoEngineFactory
from . import *

__all__ = ('OrderLineItemFactory',)

class OrderLineItemFactory(MongoEngineFactory):
    class Meta:
        model = OrderLineItem

    type = 'product'
    custom_id = factory.Sequence(lambda n: u'custom-id-{0}'.format(n))
    price = 99.50
    quantity = 1
    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    notes = u'此 Order Line Item 的備註'
