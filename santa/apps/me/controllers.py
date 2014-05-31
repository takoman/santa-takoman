# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from santa.lib.auth import AccessTokenAuth
from santa.lib.api_errors import ApiOAuthException

me = Blueprint('me', __name__)

@me.route('/api/v1/me', methods=['GET'])
def get_me():
    auth = AccessTokenAuth()
    access_token = auth.get_access_token(request)
    if not access_token:
        raise ApiOAuthException("missing access token", 401)

    user = auth.get_user_from_access_token(access_token)
    if not user:
        raise ApiOAuthException("access token is invalid or has expired", 401)

    return jsonify(email=user['email'])

@me.errorhandler(ApiOAuthException)
def handle_api_oauth_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
