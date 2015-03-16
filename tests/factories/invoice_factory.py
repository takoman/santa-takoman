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
    # TODO: We should just have an invoice reference in invoice line item.
    # https://github.com/takoman/santa/issues/119
    invoice_line_items = []
    total = 0.00
    status = 'draft'
    notes = '不隨便的 invoice 備註'
    due_at = datetime.datetime.now() + datetime.timedelta(days=7)
