# -*- coding: utf-8 -*-

import factory, datetime
from santa.models.domain import *
from factory.mongoengine import MongoEngineFactory
from . import *

__all__ = ('InvoiceFactory',)

class InvoiceFactory(MongoEngineFactory):
    class Meta:
        model = Invoice

    order = factory.SubFactory(OrderFactory)
    total = 0.00
    status = 'draft'
    notes = '不隨便的 invoice 備註'
    due_at = datetime.datetime.utcnow() + datetime.timedelta(days=7)
