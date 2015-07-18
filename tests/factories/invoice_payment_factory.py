# -*- coding: utf-8 -*-

import factory
from santa.models.domain import *
from factory.mongoengine import MongoEngineFactory
from . import *

__all__ = ('InvoicePaymentFactory',)

class AllPayATMOfflinePaymentDetailsFactory(MongoEngineFactory):
    class Meta:
        model = AllPayOfflinePaymentDetails

    merchant_id       = factory.Sequence(lambda n: 'mid-{0}'.format(n))
    merchant_trade_no = factory.Sequence(lambda n: 'mtn-{0}'.format(n))
    return_code       = 2
    return_message    = 'Get VirtualAccount Succeed'
    trade_no          = factory.Sequence(lambda n: 'tn-{0}'.format(n))
    trade_amount      = 1000.00
    payment_type      = 'ATM_TAISHIN'
    trade_date        = '2012/03/15 18:03:12'
    expire_date       = '2012/03/22 18:03:12'

    # When ChoosePayment is ATM
    bank_code         = '812'
    v_account         = '9103522175887271'

class AllPayPaymentDetailsFactory(MongoEngineFactory):
    class Meta:
        model = AllPayPaymentDetails

    merchant_id       = factory.Sequence(lambda n: 'mid-{0}'.format(n))
    merchant_trade_no = factory.Sequence(lambda n: 'mtn-{0}'.format(n))
    return_code       = 1
    return_message    = 'paid'
    trade_no          = factory.Sequence(lambda n: 'tn-{0}'.format(n))
    trade_amount      = 1000.00
    payment_date      = '2012/03/16 12:03:12'
    payment_type      = 'ATM_TAISHIN'
    payment_type_charge_fee = 25.00
    trade_date        = '2012/03/15 18:03:12'
    simulate_paid     = 0

class InvoicePaymentFactory(MongoEngineFactory):
    class Meta:
        model = InvoicePayment

    external_id = factory.Sequence(lambda n: '{0}'.format(n))
    invoice = factory.SubFactory(InvoiceFactory)
    payment_account = factory.SubFactory(AllPayAccountFactory)
    total = 1000.00
    result = 'success'
    message = u'付款成功'
    details = factory.SubFactory(AllPayPaymentDetailsFactory)
    allpay_offline_payment_details = factory.SubFactory(AllPayATMOfflinePaymentDetailsFactory)
