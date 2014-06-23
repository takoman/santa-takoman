# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from santa.lib.auth import AccessTokenAuth
from santa.lib.api_errors import ApiException
from bson.objectid import ObjectId
from santa.models.domain.user import User
from santa.lib.common import parse_request, render_json, me_to_json
import json

users = Blueprint('users', __name__)

@users.route('/api/v1/users', methods=['GET'])
def get_users():
    users = User.objects.all()

    # flask.jsonify prevents us from jsonifying a list for security reasons
    # https://github.com/mitsuhiko/flask/issues/170
    return render_json(me_to_json(users))

@users.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.objects(id=user_id).first()

    return render_json(me_to_json(users))

@users.route('/api/v1/users', methods=['POST'])
def post():
    data = parse_request(request)
    new_user = User(**data)
    new_user.save()

    return 'OK'

@users.route('/api/v1/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    data = parse_request(request)

    # Filter unknown fields
    known_fields = User._fields.keys()

    # Mongoengine update doesn't support validation now
    # https://github.com/MongoEngine/mongoengine/issues/453
    #set_user = dict((("set__%s" % k, v) for k,v in data.iteritems() if k in known_fields))
    #User.objects(id=user_id).update(**set_user)

    # So, we use save()
    user = User.objects(id=user_id).first()
    if not user:
        raise ApiException("user not found")

    for k, v in data.iteritems():
        if k in known_fields:
            setattr(user, k, v)
    user.save()

    return render_json(me_to_json(user))

@users.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.objects(id=user_id).first()
    if not user:
        raise ApiException("user not found")
    user.delete()

    return render_json(me_to_json(user))
