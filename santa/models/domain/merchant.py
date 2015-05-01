# -*- coding: utf-8 -*-

from mongoengine import *
from santa.models.mixins.updated_at_mixin import UpdatedAtMixin
from santa.models.domain import *
import datetime, pycountry

__all__ = ('Merchant',)

SUPPORTED_COUNTRIES = [c.alpha2.encode('utf-8') for c in pycountry.countries]

#
# merchant (noun)
#   :someone who buys and sells goods especially in large amounts; dealer; trader.
#

class Merchant(UpdatedAtMixin, Document):
    user              = ReferenceField(User, required=True)
    merchant_name     = StringField(required=True)
    source_countries  = ListField(StringField(choices=SUPPORTED_COUNTRIES))
    # allpay_account  = ReferenceField(PaymentAccount)
    updated_at        = DateTimeField(default=datetime.datetime.utcnow)
    created_at        = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'merchants'
    }

    def send_welcome_email(self):
        pass
