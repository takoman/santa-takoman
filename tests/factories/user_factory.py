# -*- coding: utf-8 -*-

import factory
from santa.models.domain import *
from factory.mongoengine import MongoEngineFactory
from . import *

__all__ = ('UserFactory',)

class UserFactory(MongoEngineFactory):
    class Meta:
        model = User

    name = factory.Sequence(lambda n: u'塔克超人{0}號'.format(n))
    email = factory.Sequence(lambda n: 'user-{0}@gmail.com'.format(n))
    password = 'password'
    role = [u'user']
