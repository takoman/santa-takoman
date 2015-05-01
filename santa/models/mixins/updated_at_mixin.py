# -*- coding: utf-8 -*-

from mongoengine import *
from mongoengine import signals
import datetime

class UpdatedAtMixin(object):

    @classmethod
    def update_updated_at(cls, sender, document, **kwargs):
        if issubclass(sender, cls):
            document.updated_at = datetime.datetime.utcnow()

signals.pre_save.connect(UpdatedAtMixin.update_updated_at)
