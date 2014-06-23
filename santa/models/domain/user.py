# -*- coding: utf-8 -*-

from mongoengine import *
import datetime

class User(Document):
    name        = StringField(max_length=200, required=True)
    email       = EmailField(max_length=200, required=True, unique=True)
    password    = StringField(max_length=200)
    slug        = StringField(max_length=200)
    role        = ListField(StringField(choices=[u'user', u'takoman', u'admin']))
    updated_at  = DateTimeField(default=datetime.datetime.now)
    created_at  = DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'users'
    }
