# -*- coding: utf-8 -*-

from mongoengine import *
from mongoengine import signals
import datetime
from santa.models.mixins.updated_at_mixin import UpdatedAtMixin
from santa.models.domain.order import Order

__all__ = ('AllPayOfflinePaymentDetails', 'AllPayPaymentDetails', 'OrderPayment')

SUPPORTED_PAYMENT_METHODS = [
    u'ALLPAY'
]

class AllPayOfflinePaymentDetails(EmbeddedDocument):
    merchant_id       = StringField(max_length=10)
    merchant_trade_no = StringField(max_length=20)
    return_code       = IntField()
    return_message    = StringField(max_length=200)
    trade_no          = StringField(max_length=20)
    trade_amount      = FloatField()
    payment_type      = StringField(max_length=20)
    trade_date        = DateTimeField()
    check_mac_value   = StringField()
    expire_date       = DateTimeField()

    # When ChoosePayment is ATM
    bank_code         = StringField(max_length=10)
    v_account         = StringField(max_length=20)

    # When ChoosePayment is CVS or BARCODE
    payment_no        = StringField(max_length=20)
    barcode_1         = StringField(max_length=20)
    barcode_2         = StringField(max_length=20)
    barcode_3         = StringField(max_length=20)

class AllPayPaymentDetails(EmbeddedDocument):
    merchant_id       = StringField(max_length=10)
    merchant_trade_no = StringField(max_length=20)
    return_code       = IntField()
    return_message    = StringField(max_length=200)
    trade_no          = StringField(max_length=200)
    trade_amount      = FloatField()
    payment_date      = DateTimeField()
    payment_type      = StringField(max_length=20)
    payment_type_charge_fee = FloatField()
    trade_date        = DateTimeField()
    simulate_paid     = IntField()
    check_mac_value   = StringField()
    offline_payment_details = EmbeddedDocumentField(AllPayOfflinePaymentDetails)

class OrderPayment(UpdatedAtMixin, Document):
    external_id = StringField(required=True)  # MerchantTradeNo
    order       = ReferenceField(Order)
    total       = FloatField()
    result      = StringField(choices=[u'success', u'failure'])
    message     = StringField()
    updated_at  = DateTimeField(default=datetime.datetime.now)
    created_at  = DateTimeField(default=datetime.datetime.now)
    details     = GenericEmbeddedDocumentField()

    @classmethod
    def update_order_status(cls, sender, document, **kwargs):
        payment = document
        if payment.result == u'success' and payment.order.status in ['new', 'invoiced']:
            payment.order.status = u'paid'
            payment.order.save()

signals.post_save.connect(OrderPayment.update_order_status, sender=OrderPayment)
