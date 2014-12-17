# -*- coding: utf-8 -*-

from mongoengine import *

class Image(EmbeddedDocument):
    image_url      = URLField()
    image_versions = ListField(StringField(choices=[u'small', u'medium', u'large', u'original']), default=[u'original'])
