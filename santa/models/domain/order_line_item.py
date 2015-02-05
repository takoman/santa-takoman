# -*- coding: utf-8 -*-

from mongoengine import *
from mongoengine import signals
import datetime
from santa.models.mixins.updated_at_mixin import UpdatedAtMixin
from santa.models.domain.product import Product
from santa.models.domain.order import Order

__all__ = ('OrderLineItem',)

class OrderLineItem(UpdatedAtMixin, Document):
    type        = StringField(choices=[u'product', u'commission', u'shipping_dom_a',
                                       u'shipping_intl', u'shipping_dom_b', u'tax',
                                       u'discount', u'coupon', u'fee'])
    custom_id   = StringField()  # Merchant-defined ID, e.g. coupon code.
    price       = FloatField()   # In target currency.
    quantity    = IntField()
    order       = ReferenceField(Order, required=True)
    product     = ReferenceField(Product)  # A line item can be associated with a product or not.
    notes       = StringField()
    updated_at  = DateTimeField(default=datetime.datetime.now)
    created_at  = DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'order_line_items'
    }

    @classmethod
    def update_order_total(cls, sender, document, **kwargs):
        line_item = document
        line_item.order.save()

signals.post_save.connect(OrderLineItem.update_order_total, sender=OrderLineItem)
# TODO: We should update the total when an order line item is created/updated/deleted.
