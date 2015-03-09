# -*- coding: utf-8 -*-

from mongoengine import *
from mongoengine import signals
import datetime
from santa.models.mixins.updated_at_mixin import UpdatedAtMixin
from santa.models.domain import *

__all__ = ('Invoice',)

INVOICE_STATUSES = [
    'draft', 'unpaid', 'paid', 'overdue', 'void'
]

class Invoice(UpdatedAtMixin, Document):
    invoice_no          = SequenceField(value_decorator=lambda x: "%012d" % (x,))
    order               = ReferenceField(Order, required=True)
    invoice_line_items  = ListField(ReferenceField('InvoiceLineItem'))
    total               = FloatField()  # in target currency
    status              = StringField(choices=INVOICE_STATUSES, default='draft')
    notes               = StringField()
    # invoiced_at       = DateTimeField(default=datetime.datetime.now)  # Should be the same as created_at now.
    due_at              = DateTimeField(default=datetime.datetime.now)
    created_at          = DateTimeField(default=datetime.datetime.now)
    updated_at          = DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'invoices'
    }

    @classmethod
    def update_total(cls, sender, document, **kwargs):
        invoice = document
        invoice.total = invoice.calculate_total()
        return

    def calculate_total(self):
        return sum([item.price * item.quantity for item in self.invoice_line_items])

signals.pre_save_post_validation.connect(Invoice.update_total, sender=Invoice)
