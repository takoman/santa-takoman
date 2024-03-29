# -*- coding: utf-8 -*-

import factory
from santa.models.domain import *
from factory.mongoengine import MongoEngineFactory
from . import *

__all__ = ('OrderFactory',)

class OrderFactory(MongoEngineFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(UserFactory)
    merchant = factory.SubFactory(MerchantFactory)
    total = 0.00
    currency_source = 'USD'
    currency_target = 'TWD'
    exchange_rate = 30.00
    notes = 'Random notes'
