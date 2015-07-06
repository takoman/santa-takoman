# -*- coding: utf-8 -*-

from mongoengine import *
from mongoengine import signals
import datetime
from santa.models.mixins.updated_at_mixin import UpdatedAtMixin
from santa.models.domain import *

__all__ = ('InvoiceLineItem',)

class InvoiceLineItem(UpdatedAtMixin, Document):
    invoice         = ReferenceField('Invoice', required=True)
    order_line_item = ReferenceField(OrderLineItem, required=True)
    price           = FloatField()  # In target currency.
    quantity        = IntField()
    notes           = StringField()
    updated_at      = DateTimeField(default=datetime.datetime.utcnow)
    created_at      = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'invoice_line_items'
    }

    @classmethod
    def update_invoice_total(cls, sender, document, **kwargs):
        line_item = document
        line_item.invoice.save()

# Update the invoice total when an invoice line item is created/updated/deleted.
signals.post_save.connect(InvoiceLineItem.update_invoice_total, sender=InvoiceLineItem)
