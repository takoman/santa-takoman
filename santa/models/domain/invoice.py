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
    invoice_line_items  = ListField(ReferenceField(InvoiceLineItem), default=[])
    total               = FloatField()  # in target currency
    status              = StringField(choices=INVOICE_STATUSES, default='draft')
    notes               = StringField()
    # invoiced_at       = DateTimeField(default=datetime.datetime.utcnow)  # Should be the same as created_at now.
    due_at              = DateTimeField(default=datetime.datetime.utcnow)
    created_at          = DateTimeField(default=datetime.datetime.utcnow)
    updated_at          = DateTimeField(default=datetime.datetime.utcnow)

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

    @classmethod
    def create_invoice_line_items_from_order(cls, sender, document, created, **kwargs):
        """Automatically create invoice line items from the order line items
        of the order when the invoice was created (not update). It only copies
        over order line items with status "new", and will change their
        statuses to "invoiced" afterwards.
        """
        if not created:
            return
        invoice = document
        order_line_items = OrderLineItem.objects(order=invoice.order, status='new')
        for order_line_item in order_line_items:
            InvoiceLineItem(invoice=invoice,
                            order_line_item=order_line_item,
                            price=order_line_item.price,
                            quantity=order_line_item.quantity,
                            notes=order_line_item.notes
                            ).save()
            order_line_item.update(status='invoiced')

signals.pre_save.connect(Invoice.update_total, sender=Invoice)
signals.post_save.connect(Invoice.create_invoice_line_items_from_order, sender=Invoice)
