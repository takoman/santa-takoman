# -*- coding: utf-8 -*-

import factory
from santa.models.domain import *
from factory.mongoengine import MongoEngineFactory
from . import *

__all__ = ('InvoiceLineItemFactory',)

class InvoiceLineItemFactory(MongoEngineFactory):
    class Meta:
        model = InvoiceLineItem

    invoice = factory.SubFactory(InvoiceFactory)
    order_line_item = factory.SubFactory(OrderLineItemFactory)
    price = 99.50
    quantity = 1
    notes = u'此商品已包含運費'
