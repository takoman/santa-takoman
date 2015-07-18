# -*- coding: utf-8 -*-

from mongoengine import *
import pycountry

__all__ = ('Location',)

SUPPORTED_COUNTRIES = [c.alpha2.encode('utf-8') for c in pycountry.countries]

class Location(EmbeddedDocument):
    address = StringField()
    address_2 = StringField()
    district = StringField()
    city = StringField()
    region = StringField()  # e.g. state
    zipcode = StringField()
    coordinates = PointField()
    country = StringField(choices=SUPPORTED_COUNTRIES)
