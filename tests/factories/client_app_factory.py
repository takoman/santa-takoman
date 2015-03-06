# -*- coding: utf-8 -*-

import factory
from santa.models.domain import *
from factory.mongoengine import MongoEngineFactory
from . import *

__all__ = ('ClientAppFactory',)

class ClientAppFactory(MongoEngineFactory):
    class Meta:
        model = ClientApp

    name = factory.Sequence(lambda n: u'client-app-{0}'.format(n))
