# -*- coding: utf-8 -*-

from mongoengine import *
from santa.models.domain.image import Image
import datetime

class Product(Document):
    title             = StringField(max_length=200, required=True)
    seller_product_id = StringField(max_length=40)  # Product ID from the seller to helpidentify the same product, e.g. ASIN on Amazon.
    brand             = StringField(max_length=200)
    color             = StringField(max_length=40)
    size              = StringField(max_length=40)
    images            = ListField(EmbeddedDocumentField(Image, default=Image))
    urls              = ListField(URLField())
    description       = StringField()  # Public product description
    notes             = StringField()  # Product notes, for internal use
    updated_at        = DateTimeField(default=datetime.datetime.now)
    created_at        = DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'products'
    }
