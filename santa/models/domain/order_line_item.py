# -*- coding: utf-8 -*-

from mongoengine import *
from mongoengine import signals
import datetime
from santa.models.mixins.updated_at_mixin import UpdatedAtMixin
from santa.models.domain.product import Product
from santa.models.domain.order import Order

__all__ = ('OrderLineItem',)

ORDER_LINE_ITEM_STATUSES = [
    u'new',
    u'invoiced'  # it has been converted into an invoice line item, and cannot be modified
]

class OrderLineItem(UpdatedAtMixin, Document):
    type        = StringField(choices=[u'product', u'commission', u'shipping',
                                       u'tax', u'discount', u'coupon', u'fee'])
    custom_id   = StringField()  # Merchant-defined ID, e.g. coupon code.
    price       = FloatField()   # In target currency.
    quantity    = IntField()
    order       = ReferenceField(Order, required=True)
    product     = ReferenceField(Product)  # A line item can be associated with a product or not.
    status      = StringField(choices=ORDER_LINE_ITEM_STATUSES, default=u'new')
    notes       = StringField()
    updated_at  = DateTimeField(default=datetime.datetime.utcnow)
    created_at  = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'order_line_items'
    }

    @classmethod
    def update_order_total(cls, sender, document, **kwargs):
        line_item = document
        line_item.order.save()

# Update the order total when an order line item is created/updated/deleted.
signals.post_save.connect(OrderLineItem.update_order_total, sender=OrderLineItem)
signals.post_delete.connect(OrderLineItem.update_order_total, sender=OrderLineItem)
