# -*- coding: utf-8 -*-

from mongoengine import *
import datetime

class SocialAuth(Document):
    # always required
    uid         = StringField(max_length=200, required=True)
    user        = ReferenceField('User')

    # sometimes supplied, depending on the provider
    name        = StringField(max_length=200)
    email       = EmailField(max_length=200)
    first_name  = StringField(max_length=200)
    last_name   = StringField(max_length=200)
    nickname    = StringField(max_length=200)
    location    = StringField()
    description = StringField()
    image       = StringField()
    phone       = StringField()
    urls        = DictField()
    credentials = DictField()
    extra       = DictField()

    updated_at  = DateTimeField(default=datetime.datetime.now)
    created_at  = DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'social_auths'
    }
