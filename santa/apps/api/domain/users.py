# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from santa.lib.auth import AccessTokenAuth
from santa.lib.api_errors import ApiException
from bson.objectid import ObjectId
from santa.models.domain.user import User
from santa.models.domain.social_auth import SocialAuth
from santa.lib.common import parse_request, render_json, me_to_json
from santa.lib.auth import require_app_auth
from santa.lib.social_auth import SocialFacebook
import json

users = Blueprint('users', __name__)

@users.route('/api/v1/users', methods=['GET'])
@require_app_auth
def get_users():
    users = User.objects.all()

    # flask.jsonify prevents us from jsonifying a list for security reasons
    # https://github.com/mitsuhiko/flask/issues/170
    return render_json(me_to_json(users))

@users.route('/api/v1/users/<user_id>', methods=['GET'])
@require_app_auth
def get_user(user_id):
    user = User.objects(id=user_id).first()

    return render_json(me_to_json(users))

#
# We use the /users endpoints for both credentials and oauth token signups.
#
@users.route('/api/v1/users', methods=['POST'])
@require_app_auth
def post():
    data = parse_request(request)

    # If signing up via oauth tokens
    if data.get('provider') and data.get('oauth_token'):
        if data.get('provider') == 'facebook':
            auth_data = SocialFacebook().get_auth_data(data.get('oauth_token'))
        else:
            raise ApiException("unsupported oauth provider")

        if not auth_data:
            raise ApiException("invalid oauth token")

        matching_auth = SocialAuth.objects(uid=auth_data.get('uid')).first()
        if matching_auth:
            raise ApiException(
                "another account has already been linked" +
                ", uid=" + auth_data.get('uid') +
                ", name=" + auth_data.get('name') +
                ", email=" + auth_data.get('email')
            )

    # If signing up via credentials
    elif all([data.get('email'), data.get('password'), data.get('name')]):
        pass
    else:
        raise ApiException("unsupported signup type")

    email = data.get('email') or (auth_data and auth_data.get('email'))
    data['email'] = email

    new_user = User(**data)
    new_user.save()
    if data.get('provider') and data.get('oauth_token'):
        new_user.link_social_auth(auth_data)
    new_user.send_welcome_email()

    return render_json(me_to_json(new_user))

@users.route('/api/v1/users/<user_id>', methods=['PUT'])
@require_app_auth
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
@require_app_auth
def delete_user(user_id):
    user = User.objects(id=user_id).first()
    if not user:
        raise ApiException("user not found")
    user.delete()

    return render_json(me_to_json(user))
