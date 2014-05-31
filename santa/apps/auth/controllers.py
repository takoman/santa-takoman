# -*- coding: utf-8 -*-
from flask import current_app as app
from flask import Blueprint, request, jsonify
from santa.lib.user_trust import UserTrust
from santa.lib.api_errors import ApiOAuthException
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
            'user': user, 'application': client_app, 'expires_in': expires_in
        })

#    elif grant_type == 'oauth_token':
#        oauth_provider = form.get('oauth_provider')
#        if not oauth_provider:
#            raise ApiOAuthException("missing oauth provider")
#
#        oauth_token = form.get('oauth_token')
#        if not oauth_token:
#            raise ApiOAuthException("missing oath token")
#
#        if oauth_provide == 'facebook':
#            auth_data = SocialFacebook.get_auth_data(oauth_token)
#        else:
#            raise ApiOAuthException("unsupported oauth provider")
#
#        matching_auth = Authentication.find_by_auth_data(auth_data)
#        if not matching_auth or not matching_auth.user:
#            raise ApiOAuthException(
#                "no account linked to oauth token" +
#                ", id=" + auth_data.uid +
#                ", name=" + auth_data.name +
#                ", email=" + auth_date.email
#            )
#        access_token = UserTrust().create_access_token({
#            'user': matching_auth.user, 'application': application, 'expires_in': expires_in
#        })
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
