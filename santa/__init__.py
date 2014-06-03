import os, json, datetime, bcrypt
from eve import Eve
from eve.utils import config
from santa.lib.auth import XAppTokenAuth
from flask import current_app as app
from flask import jsonify
from apps.auth.controllers import auth
from apps.me.controllers import me
from bson.objectid import ObjectId
from santa.lib.social_auth import SocialFacebook
from santa.lib.api_errors import ApiException

def create_app():
    # The way how Eve looks for the abs settings file would not work when working
    # with gunicorn (will look for venv/bin/settings.py). So we provide the abs
    # explicitly here. Considering making a PR later.
    # https://github.com/nicolaiarocci/eve/blob/develop/eve/flaskapp.py#L171
    current_dir = os.path.dirname(os.path.realpath(__file__))
    app = Eve(auth=XAppTokenAuth, settings=current_dir + '/../config/settings.py')

    hook_up_error_handlers(app)
    hook_up_callbacks(app)
    register_apps(app)
    return app

def hook_up_error_handlers(app):
    @app.errorhandler(ApiException)
    def handle_api_oauth_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

# Hook up additional Flask controllers
def register_apps(app):
    app.register_blueprint(auth)
    app.register_blueprint(me)

def hook_up_callbacks(app):
    app.on_post_GET_client_apps += process_client_app_token
    app.on_pre_POST_users += validate_user
    app.on_insert_users += normalize_user

def process_client_app_token(request, payload):
    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')

    lookup = { 'client_id': client_id, 'client_secret': client_secret }
    clients = app.data.driver.db['client_apps']
    client = clients.find_one(lookup)

    payload.set_data('{}')
    if client:
        # Ideally, we have to expire tokens periodically and generate new ones.
        # Here we just expire it in 10 years.
        ten_years_from_now = datetime.datetime.now() + datetime.timedelta(days=10 * 365)
        expires = ten_years_from_now.isoformat()
        data = { u'xapp_token': client['token'], u'expires_in': expires }
        payload.set_data(json.dumps(data))

#
# We use the /users endpoints for both credentials and oauth token signups.
# The conditions are too complex, so we validate the request here at once,
# instead of using Eve's data validation.
#
def validate_user(request):
    data = request.form or request.json
    print data
    # TODO prevent logged in users from creating other users?

    # If signing up via oauth tokens
    if data.get('provider') and data.get('oauth_token'):
        if data.get('provider') == 'facebook':
            auth_data = SocialFacebook().get_auth_data(data.get('oauth_token'))
        else:
            raise ApiException("unsupported oauth provider")

        if not auth_data:
            raise ApiException("invalid oauth token")

        social_auths = app.data.driver.db['social_authentications']
        matching_auth = social_auths.find_one({'uid': auth_data.get('uid')})
        if matching_auth:
            raise ApiException(
                "another acount has already been linked" +
                ", uid=" + auth_data.get('uid') +
                ", name=" + auth_data.get('name') +
                ", email=" + auth_data.get('email')
            )
    # Or via credentials
    else:
        password = data.get('password')
        if not password:
            raise ApiException("missing password")
        if len(password) < 8:
            raise ApiException("password must be at least 8 characters")

    email = data.get('email') or (auth_data and auth_data.get('email'))
    # If both email in credentials and in oauth data are missing
    if not email:
        raise ApiException("missing email")

    users = app.data.driver.db['users']
    user = users.find_one({'email': email})
    # A user's email needs to be unique no matter it's from credentials or oauth
    if user:
        raise ApiException("user already exists with email " + email)

#
# Normalize user data before inserting to database. If the request is from
# social signup, create social auth and associate it with the user.
#
def normalize_user(users):
    for user in users:
        # We need the user's object id when linking to her social auth below,
        # so we manually assign the _id to be used in the mongo db later.
        user['_id'] = ObjectId(user.get('_id')) or ObjectId()

        if 'password' in user:
            # encrypt password
            user['password'] = bcrypt.hashpw(user['password'], bcrypt.gensalt())

        # normalize email
        # TODO We need to somehow reuse the auth_data retrieved in validate_user.
        auth_data = SocialFacebook().get_auth_data(user.get('oauth_token'))
        email = user.get('email') or (auth_data and auth_data.get('email'))
        user['email'] = email.lower()

        # link social account
        if user.get('provider') and user.get('oauth_token'):
            data = {'uid': auth_data.get('uid'), 'user': user['_id']}
            if 'info' in auth_data:
                for field in ['name', 'email', 'nickname', 'first_name', 'last_name', 'location', 'description', 'image', 'phone']:
                    data[field] = auth_data['info'].get(field)
                if auth_data['info'].get('urls'):
                    data['urls'] = auth_data['info'].get('urls')

            if 'credentials' in auth_data:
                data['credentials'] = auth_data['credentials']

            # TODO flush any complex objects from extra hash
            if 'extra' in auth_data:
                pass

            # need to manually add the _created and _updated timestamps
            date_utc = datetime.datetime.utcnow().replace(microsecond=0)
            data[config.LAST_UPDATED] = data[config.DATE_CREATED] = date_utc
            social_auths = app.data.driver.db['social_authentications']
            social_auths.insert(data)

        # remove unnecessary fields
        user.pop('provider', None)
        user.pop('oauth_token', None)
