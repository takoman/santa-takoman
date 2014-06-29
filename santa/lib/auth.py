import bcrypt
from flask import request, Response, abort, current_app as app
from santa.lib.user_trust import UserTrust
from santa.lib.api_errors import ApiException
from santa.models.domain.client_app import ClientApp
from functools import wraps

def require_auth(f, auth_class):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = auth_class()
        roles = resource_name = None
        if not auth.authorized(roles, resource_name, request.method):
            return auth.authenticate()
        return f(*args, **kwargs)

    return decorated

def require_app_auth(f):
    return require_auth(f, XAppTokenAuth)

class BasicAuth(object):
    """ Implements Basic AUTH logic. Should be subclassed to implement custom
    authentication checking.
    """
    def check_auth(self, username, password, allowed_roles, resource, method):
        """ This function is called to check if a username / password
        combination is valid. Must be overridden with custom logic.

        :param username: username provided with current request.
        :param password: password provided with current request
        :param allowed_roles: allowed user roles.
        :param resource: resource being requested.
        :param method: HTTP method being executed (POST, GET, etc.)
        """
        raise NotImplementedError

    def authenticate(self):
        """ Returns a standard a 401 response that enables basic auth.
        Override if you want to change the response and/or the realm.
        """
        resp = Response(None, 401, {'WWW-Authenticate': 'Basic realm:"%s"' %
                                    __package__})
        abort(401, description='Please provide proper credentials',
              response=resp)

    def authorized(self, allowed_roles, resource, method):
        """ Validates the the current request is allowed to pass through.

        :param allowed_roles: allowed roles for the current request, can be a
                              string or a list of roles.
        :param resource: resource being requested.
        """
        auth = request.authorization
        return auth and self.check_auth(auth.username, auth.password,
                                        allowed_roles, resource, method)

class TokenAuth(BasicAuth):
    """ Implements Token AUTH logic. Should be subclassed to implement custom
    authentication checking.
    """
    def check_auth(self, token, allowed_roles, resource, method):
        """ This function is called to check if a token is valid. Must be
        overridden with custom logic.

        :param token: decoded user name.
        :param allowed_roles: allowed user roles
        :param resource: resource being requested.
        :param method: HTTP method being executed (POST, GET, etc.)
        """
        raise NotImplementedError

    def authenticate(self):
        """ Returns a standard a 401 response that enables basic auth.
        Override if you want to change the response and/or the realm.
        """
        resp = Response(None, 401, {'WWW-Authenticate': 'Basic realm:"%s"' %
                                    __package__})
        abort(401, description='Please provide proper credentials',
              response=resp)

    def authorized(self, allowed_roles, resource, method):
        """ Validates the the current request is allowed to pass through.

        :param allowed_roles: allowed roles for the current request, can be a
                              string or a list of roles.
        :param resource: resource being requested.
        """
        auth = request.authorization
        return auth and self.check_auth(auth.username, allowed_roles, resource,
                                        method)

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
        auth = (request.args.get('xapp_token') or
                request.form.get('xapp_token') or
                (request.json and request.json.get('xapp_token')) or
                request.headers.get('X-XAPP-TOKEN'))
        return auth and self.check_auth(auth, allowed_roles, resource, method)

    def check_auth(self, token, allowed_roles, resource, method):
        return ClientApp.objects(token=token).first()

    def authenticate(self):
        """ Returns a standard a 401 response that enables xapp auth.
        Override if you want to change the response and/or the realm.
        """
        raise ApiException("please provide proper credentials", 401)

class AccessTokenAuth(TokenAuth):
    def authorized(self, allowed_roles, resource, method):
        auth = self.get_access_token(request)
        return auth and self.check_auth(auth, allowed_roles, resource, method)

    def check_auth(self, token, allowed_roles, resource, method):
        return self.get_user_from_access_token(token)

    def authenticate(self):
        """ Returns a standard a 401 response that enables xapp auth.
        Override if you want to change the response and/or the realm.
        """
        raise ApiException("please provide proper credentials", 401)

    def get_access_token(self, request):
        return (request.args.get('access_token') or
                request.form.get('access_token') or
                (request.json and request.json.get('access_token')) or
                request.headers.get('X-ACCESS-TOKEN'))

    def get_user_from_access_token(self, access_token):
        user = None
        try:
            user = UserTrust().get_user_from_access_token({
                'access_token': access_token
            })
        except StandardError:
            pass

        return user
