import bcrypt
from flask import request, current_app as app
from eve.auth import BasicAuth, TokenAuth
from santa.lib.user_trust import UserTrust

class BCryptAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        users = app.data.driver.db['users']
        lookup = {'username': username}
        if allowed_roles:
            # only retrieve a user if his roles match `allowed_roles`
            lookup['roles'] = {'$in': allowed_roles}
        user = users.find_one(lookup)
        return user and bcrypt.hashpw(password, user['password']) == user['password']

class XAppTokenAuth(TokenAuth):
    # Override TokenAuth to use the X-XAPP-TOKEN header
    def authorized(self, allowed_roles, resource, method):
        """ Validates the the current request is allowed to pass through.

        :param allowed_roles: allowed roles for the current request, can be a
                              string or a list of roles.
        :param resource: resource being requested.
        """
        auth  = request.args.get('xapp_token') or \
                request.form.get('xapp_token') or \
                (request.json and request.json.get('xapp_token')) or \
                request.headers.get('X-XAPP-TOKEN')
        return auth and self.check_auth(auth, allowed_roles, resource, method)

    def check_auth(self, token, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        client_apps = app.data.driver.db['client_apps']
        lookup = {'token': token}
        return client_apps.find_one(lookup)

class AccessTokenAuth(TokenAuth):
    def authorized(self, allowed_roles, resource, method):
        auth = self.get_access_token(request)
        return auth and self.check_auth(auth, allowed_roles, resource, method)

    def check_auth(self, token, allowed_roles, resource, method):
        return self.get_user_from_access_token(token)

    def get_access_token(self, request):
        return  request.args.get('access_token') or \
                request.form.get('access_token') or \
                (request.json and request.json.get('access_token')) or \
                request.headers.get('X-ACCESS-TOKEN')

    def get_user_from_access_token(self, access_token):
        user = None
        try:
            user = UserTrust().get_user_from_access_token(
                {'access_token': access_token}
            )
        except StandardError as e:
            print e

        return user
