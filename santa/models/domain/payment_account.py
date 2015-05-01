# -*- coding: utf-8 -*-

from mongoengine import *
import datetime
from santa.models.mixins.updated_at_mixin import UpdatedAtMixin
from santa.models.domain import *

__all__ = ('PaymentAccount', 'AllPayAccount')

SUPPORTED_PAYMENT_GATEWAYS = [
    'AllPay',
    # 'Stripe',
    # 'Balanced',
    # 'Paypal'
]

class PaymentAccount(UpdatedAtMixin, Document):
    # TODO: external_id should be required, but Allpay doesn't support it now.
    external_id = StringField()
    provider    = StringField(choices=SUPPORTED_PAYMENT_GATEWAYS, required=True)
    customer    = ReferenceField(User, required=True)
    updated_at  = DateTimeField(default=datetime.datetime.utcnow)
    created_at  = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'allow_inheritance': True,
        'collection': 'payment_accounts'
    }

class AllPayAccount(PaymentAccount):
    provider = StringField(default='AllPay', choices=['AllPay'])
