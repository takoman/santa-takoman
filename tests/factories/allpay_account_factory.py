# -*- coding: utf-8 -*-

import factory
from santa.models.domain import *
from factory.mongoengine import MongoEngineFactory
from . import *

__all__ = ('AllPayAccountFactory',)

class AllPayAccountFactory(MongoEngineFactory):
    class Meta:
        model = AllPayAccount

    external_id = factory.Sequence(lambda n: '{0}'.format(n))
    provider = 'AllPay'
    customer = factory.SubFactory(UserFactory)
