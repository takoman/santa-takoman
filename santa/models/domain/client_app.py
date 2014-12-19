# -*- coding: utf-8 -*-

from mongoengine import *
from santa.models.mixins.updated_at_mixin import UpdatedAtMixin
import datetime

class ClientApp(UpdatedAtMixin, Document):
    client_id       = StringField(max_length=200, required=True, unique=True)
    client_secret   = StringField(max_length=200, required=True)
    token           = StringField(max_length=200)
    updated_at      = DateTimeField(default=datetime.datetime.now)
    created_at      = DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'client_apps'
    }
