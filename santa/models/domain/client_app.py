# -*- coding: utf-8 -*-

from mongoengine import *
from mongoengine import signals
from santa.models.mixins.updated_at_mixin import UpdatedAtMixin
import datetime, os, binascii

__all__ = ('ClientApp',)

class ClientApp(UpdatedAtMixin, Document):
    name            = StringField(max_length=200, required=True)
    client_id       = StringField(max_length=200, required=True, unique=True)
    client_secret   = StringField(max_length=200, required=True)
    token           = StringField(max_length=200)
    updated_at      = DateTimeField(default=datetime.datetime.now)
    created_at      = DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'client_apps'
    }

    @classmethod
    def generate_id_and_secret(cls, sender, document, **kwargs):
        app = document
        app.client_id, app.client_secret = binascii.hexlify(os.urandom(10)), binascii.hexlify(os.urandom(16))

        # TODO: Token should not store in the document. Instead, we should
        # generate it dynamically and expire it.
        # https://github.com/artsy/gravity/blob/ccf02a6badf81f1bd96bd57009ac1392b5cb08fa/app/models/domain/client_application.rb#L61
        app.token = binascii.hexlify(os.urandom(64))

signals.pre_save.connect(ClientApp.generate_id_and_secret, sender=ClientApp)
