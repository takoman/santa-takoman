# -*- coding: utf-8 -*-

from flask import Response
from bson.objectid import ObjectId
from mongoengine import *
from mongoengine.queryset.base import BaseQuerySet
from santa.lib.util import date_to_str
from santa.lib.api_errors import ApiException
import json, datetime

class BaseJSONEncoder(json.JSONEncoder):
    """ Proprietary JSONEconder subclass used by the json render function.
    This is needed to address the encoding of special values.
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            # convert any datetime to ISO-8601 format
            return date_to_str(obj)
        elif isinstance(obj, (datetime.time, datetime.date)):
            # should not happen since the only date-like format
            # supported at domain schema level is 'datetime'.
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

class MongoJSONEncoder(BaseJSONEncoder):
    """ Proprietary JSONEconder subclass used by the json render function.
    This is needed to address the encoding of special values.
    """
    def default(self, obj):
        if isinstance(obj, ObjectId):
            # BSON/Mongo ObjectId is rendered as a string
            return str(obj)
        else:
            # delegate rendering to base class method
            return super(MongoJSONEncoder, self).default(obj)

def and_friends_to_mongo(doc):
    """ Fetch one level of reference fields, including those in lists,
    and convert them to mongo as well.
    """
    m = doc.to_mongo()
    for k in m:
        if k is '_id':
            continue
        if isinstance(m[k], ObjectId):
            m[k] = doc[k].to_mongo()
        elif isinstance(m[k], list):
            m[k] = [doc[k][i].to_mongo() if isinstance(r, ObjectId) else r for i, r in enumerate(m[k])]
    return m

def me_to_json(obj):
    """ Converts a mongoengine object to JSON string.

    :param obj: the mongoengine object to convert, can be an instance of
                Document or a BaseQuerySet.
    """
    if isinstance(obj, Document):
        return json.dumps(and_friends_to_mongo(obj), cls=MongoJSONEncoder)
    if isinstance(obj, BaseQuerySet):
        return json.dumps([and_friends_to_mongo(doc) for doc in obj], cls=MongoJSONEncoder)
    if isinstance(obj, list):
        return json.dumps(map(lambda x: and_friends_to_mongo(x), obj), cls=MongoJSONEncoder)
    raise ApiException("can't convert unsupported type to JSON")

def render_json(json, status=200):
    return Response(json, status=status, mimetype='application/json')

def parse_request(request):
    """ Performs sanity checks or decoding depending on the Content-Type,
    then returns the request payload as a dict. If request Content-Type is
    unsupported, aborts with a 400 (Bad Request).
    """
    content_type = request.headers['Content-Type'].split(';')[0]

    if content_type == 'application/json':
        return request.get_json()
    elif content_type == 'application/x-www-form-urlencoded':
        if not len(request.form):
            raise ApiException("no form-urlencoded data supplied")
        return request.form.to_dict()
    elif content_type == 'multipart/form-data':
        # as multipart is also used for file uploads, we let an empty
        # request.form go through as long as there are also files in the
        # request.
        if len(request.form) or len(request.files):
            # merge form fields and request files, so we get a single payload
            # to be validated against the resource schema.

            # list() is needed because Python3 items() returns a dict_view, not
            # a list as in Python2.
            return dict(list(request.form.to_dict().items()) +
                        list(request.files.to_dict().items()))
        else:
            raise ApiException("no multipart/form-data supplied")
    else:
        raise ApiException("unknown or no Content-Type header supplied")
