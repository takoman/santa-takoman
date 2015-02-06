# -*- coding: utf-8 -*-

import factory
from santa.models.domain import *
from factory.mongoengine import MongoEngineFactory
from . import *

__all__ = ('MerchantFactory',)

class MerchantFactory(MongoEngineFactory):
    class Meta:
        model = Merchant

    user = factory.SubFactory(UserFactory, role=[u'user', u'takoman'])
    merchant_name = factory.Sequence(lambda n: u'塔克超人{0}號的店'.format(n))
    source_countries = ['US']
