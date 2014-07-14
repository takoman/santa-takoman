# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from santa.lib.user_trust import UserTrust
from santa.lib.api_errors import ApiException
from santa.lib.social_auth import SocialFacebook
from santa.models.domain.client_app import ClientApp
from santa.models.domain.user import User
from santa.models.domain.social_auth import SocialAuth
import datetime, bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/oauth2/access_token', methods=['POST'])
def oauth():
    form = request.form or request.json
    client_id = form.get('client_id')
    if not client_id:
        raise ApiException("missing client_id")
    client_app = ClientApp.objects(client_id=client_id, client_secret=form.get('client_secret')).first()
    if not client_app:
        raise ApiException("invalid client_id or client_secret")

    expires_in = datetime.datetime.now() + datetime.timedelta(days=60)

    grant_type = form.get('grant_type')
    if grant_type == 'credentials':
        email = form.get('email')
        if not email:
            raise ApiException("missing email")

        password = form.get('password')
        if not password:
            raise ApiException("missing password")

        user = User.objects(email=email).first()
        if not user or not is_valid_password(user, password):
            raise ApiException("invalid email or password")

        access_token = UserTrust().create_access_token({
            'user': user.to_mongo(),
            'client_app': client_app.to_mongo(),
            'expires_in': expires_in
        })

    elif grant_type == 'oauth_token':
        oauth_provider = form.get('oauth_provider')
        if not oauth_provider:
            raise ApiException("missing oauth provider")

        oauth_token = form.get('oauth_token')
        if not oauth_token:
            raise ApiException("missing oauth token")

        if oauth_provider == 'facebook':
            auth_data = SocialFacebook().get_auth_data(oauth_token)
        else:
            raise ApiException("unsupported oauth provider")

        if not auth_data:
            raise ApiException("invalid oauth token")

        matching_auth = SocialAuth.objects(uid=auth_data.get('uid')).first()
        if not matching_auth or not matching_auth.user:
            raise ApiException(
                "no account linked to oauth token" +
                ", uid=" + auth_data.get('uid') +
                ", name=" + auth_data.get('name') +
                ", email=" + auth_data.get('email')
            )
        user = User.objects(id=matching_auth.user.id).first()
        if not user:
            raise ApiException("missing user associated with this oauth token")

        access_token = UserTrust().create_access_token({
            'user': user.to_mongo(),
            'client_app': client_app.to_mongo(),
            'expires_in': expires_in
        })

    else:
        raise ApiException("unsupported grant type")

    return jsonify(access_token=access_token, expires_in=expires_in.isoformat())

def is_valid_password(user, password):
    return user and bcrypt.hashpw(password, user.password) == user.password
