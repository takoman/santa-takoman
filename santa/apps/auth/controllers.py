# -*- coding: utf-8 -*-
from flask import current_app as app
from flask import Blueprint, request, jsonify
from santa.lib.user_trust import UserTrust
from santa.lib.api_errors import ApiOAuthException
from santa.lib.social_auth import SocialFacebook
import datetime, bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/oauth2/access_token', methods=['POST'])
def oauth():
    form = request.form or request.json
    client_id = form.get('client_id')
    if not client_id:
        raise ApiOAuthException("missing client_id")
    client_apps = app.data.driver.db['client_apps']
    lookup = {'client_id': client_id, 'client_secret': form.get('client_secret')}
    client_app = client_apps.find_one(lookup)
    if not client_app:
        raise ApiOAuthException("invalid client_id or client_secret")

    expires_in = datetime.datetime.now() + datetime.timedelta(days=60)

    grant_type = form.get('grant_type')
    if grant_type == 'credentials':
        email = form.get('email')
        if not email:
            raise ApiOAuthException("missing email")

        password = form.get('password')
        if not password:
            raise ApiOAuthException("missing password")

        users = app.data.driver.db['users']
        user = users.find_one({'email': email})
        if not user or not is_valid_password(user, password):
            raise ApiOAuthException("invalid email or password")

        access_token = UserTrust().create_access_token({
            'user': user, 'client_app': client_app, 'expires_in': expires_in
        })

    elif grant_type == 'oauth_token':
        oauth_provider = form.get('oauth_provider')
        if not oauth_provider:
            raise ApiOAuthException("missing oauth provider")

        oauth_token = form.get('oauth_token')
        if not oauth_token:
            raise ApiOAuthException("missing oauth token")

        if oauth_provider == 'facebook':
            auth_data = SocialFacebook().get_auth_data(oauth_token)
        else:
            raise ApiOAuthException("unsupported oauth provider")

        if not auth_data:
            raise ApiOAuthException("invalid oauth token")

        social_auths = app.data.driver.db['social_authentications']
        matching_auth = social_auths.find_one({'uid': auth_data.get('uid')})
        if not matching_auth or not matching_auth.get('user'):
            raise ApiOAuthException(
                "no account linked to oauth token" +
                ", uid=" + auth_data.get('uid') +
                ", name=" + auth_data.get('name') +
                ", email=" + auth_data.get('email')
            )
        users = app.data.driver.db['users']
        user = users.find_one({'_id': matching_auth.get('user')})
        if not user:
            raise ApiOAuthException("missing user associated with this oauth token")

        access_token = UserTrust().create_access_token({
            'user': user, 'client_app': client_app, 'expires_in': expires_in
        })

    else:
        raise ApiOAuthException("unsupported grant type")

    return jsonify(access_token=access_token, expires_in=expires_in.isoformat())

@auth.errorhandler(ApiOAuthException)
def handle_api_oauth_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def is_valid_password(user, password):
    return user and bcrypt.hashpw(password, user['password']) == user['password']
