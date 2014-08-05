# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from santa.lib.auth import AccessTokenAuth
from santa.lib.api_errors import ApiException

me = Blueprint('me', __name__)

@me.route('/me', methods=['GET'])
def get_me():
    auth = AccessTokenAuth()
    access_token = auth.get_access_token(request)
    if not access_token:
        raise ApiException("missing access token", 401)

    user = auth.get_user_from_access_token(access_token)
    if not user:
        raise ApiException("access token is invalid or has expired", 401)

    return jsonify(email=user['email'])
