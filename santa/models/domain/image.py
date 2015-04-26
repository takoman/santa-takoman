# -*- coding: utf-8 -*-

from mongoengine import *

__all__ = ('Image',)

class Image(EmbeddedDocument):
    original    = URLField()
    small       = URLField()
    medium      = URLField()
    large       = URLField()
    square      = URLField()
