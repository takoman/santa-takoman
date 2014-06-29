# -*- coding: utf-8 -*-
"""
    santa.lib.user_trust.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    'user_trust' lib for access token creation/decryption

    :copyright: (c) 2013 by Chung-Yi Chi
    :license:
"""

from flask import current_app as app
from aes_cipher import AESCipher
from santa.lib.api_errors import ApiException
from santa.models.domain.user import User
from santa.models.domain.client_app import ClientApp
import datetime, json, uuid, dateutil.parser, os, hashlib

class UserTrust:

    # Create an access token
    def create_access_token(self, options):
        user = options.get('user')
        if not user:
            raise ApiException("missing user")

        data = {}
        data['user_id'] = user.get('email')
        if 'client_app' in options:
            data['app_id'] = options['client_app'].get('client_id')

        expires_in = options.get(
            'expires_in',
            datetime.datetime.today() + datetime.timedelta(days=1)
        )

        raw = dict({
            'expires_in': expires_in.isoformat(),
            'salt': str(uuid.uuid4())  # random uuid
        }.items() + data.items())

        aes = AESCipher(self.secret_key())
        return aes.encrypt(json.dumps(raw))

    # Return a user extracted from the access token
    def get_user_from_access_token(self, options):
        access_token = options.get('access_token')
        if not access_token:
            raise ApiException("missing access token")

        trust_str = AESCipher(self.secret_key()).decrypt(access_token.encode('utf-8'))
        trust = json.loads(trust_str)

        expires_in_str = trust.get('expires_in')
        if not expires_in_str:
            raise ApiException("missing expires in the trust token")

        if datetime.datetime.now() > dateutil.parser.parse(expires_in_str):
            raise ApiException("token expired: " + ", ".join(
                filter(None, map(
                    lambda x: x[0] + "=" + x[1] if x[0] != 'salt' else '', trust.items()
                ))))

        user_id = trust.get('user_id')
        if not user_id:
            raise ApiException("missing user_id in the trust token")

        client_id = trust.get('app_id')
        client_app = ClientApp.objects(client_id=client_id).first()
        if not client_id or not client_app:
            return None

        user = User.objects(email=user_id).first()
        if not user:
            return None

        return user.to_mongo()

    def secret_key(self):
        trust_key_value = os.environ.get('TOKEN_TRUST_KEY') or app.config.get('TOKEN_TRUST_KEY')
        if not trust_key_value:
            raise ApiException("missing trust token key")

        # using hexdigest() would generate 64 bytes string
        # and the AES encoding will fail.
        return hashlib.sha256(trust_key_value).digest()

if __name__ == '__main__':
    trust = UserTrust()
    access_token = trust.create_access_token({
        'user': {'_id': 'takoman'},
        'client_app': {'_id': 'rudy'},
        'expires_in': datetime.datetime.today() + datetime.timedelta(days=-7)
    })
    print trust.get_user_from_access_token({'access_token': access_token})
