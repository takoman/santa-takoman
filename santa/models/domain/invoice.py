# -*- coding: utf-8 -*-

from mongoengine import *
from mongoengine import signals
from santa.models.mixins.updated_at_mixin import UpdatedAtMixin
from santa.models.domain import *
import os, datetime, binascii

__all__ = ('Invoice',)

INVOICE_STATUSES = [
    'draft', 'unpaid', 'paid', 'overdue', 'void'
]

class Invoice(UpdatedAtMixin, Document):
    invoice_no          = SequenceField(value_decorator=lambda x: "%012d" % (x,))
    order               = ReferenceField(Order, required=True)
    invoice_line_items  = ListField(ReferenceField(InvoiceLineItem), default=[])
    total               = FloatField()  # in target currency
    status              = StringField(choices=INVOICE_STATUSES, default='draft')
    notes               = StringField()
    # invoiced_at       = DateTimeField(default=datetime.datetime.utcnow)  # Should be the same as created_at now.
    due_at              = DateTimeField(default=datetime.datetime.utcnow)
    access_key          = StringField()
    created_at          = DateTimeField(default=datetime.datetime.utcnow)
    updated_at          = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'invoices'
    }

    @classmethod
    def set_access_key(cls, sender, document, **kwargs):
        invoice = document
        if not invoice.access_key:
            invoice.access_key = binascii.hexlify(os.urandom(24))

    @classmethod
    def update_total(cls, sender, document, **kwargs):
        invoice = document
        invoice.total = invoice.calculate_total()
        return

    def calculate_total(self):
        return sum([item.price * item.quantity for item in self.invoice_line_items])

    def create_invoice_line_items(self):
        """Create invoice line items from the order line items of the order.
        It only copies over order line items with status "new", and will
        change their statuses to "invoiced".
        """
        order_line_items = OrderLineItem.objects(order=self.order, status='new')
        for order_line_item in order_line_items:
            InvoiceLineItem(invoice=self,
                            order_line_item=order_line_item,
                            price=order_line_item.price,
                            quantity=order_line_item.quantity,
                            notes=order_line_item.notes
                            ).save()
            order_line_item.update(status='invoiced')

    @classmethod
    def create_invoice_and_line_items_from_order(cls, order, other_attrs):
        attrs = { k: v for (k, v) in other_attrs.iteritems() if k in cls._fields.keys() }
        attrs.update({'order': order, 'status': 'unpaid'})
        new_invoice = cls(**attrs).save()
        new_invoice.create_invoice_line_items()
        new_invoice.order.update(status='invoiced')
        new_invoice.reload()
        return new_invoice

signals.pre_save.connect(Invoice.update_total, sender=Invoice)
signals.pre_save.connect(Invoice.set_access_key, sender=Invoice)
