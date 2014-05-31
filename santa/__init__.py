import os, json, datetime, bcrypt
from eve import Eve
from santa.lib.auth import XAppTokenAuth
from flask import current_app as app
from apps.auth.controllers import auth

def create_app():
    # The way how Eve looks for the abs settings file would not work when working
    # with gunicorn (will look for venv/bin/settings.py). So we provide the abs
    # explicitly here. Considering making a PR later.
    # https://github.com/nicolaiarocci/eve/blob/develop/eve/flaskapp.py#L171
    current_dir = os.path.dirname(os.path.realpath(__file__))
    app = Eve(auth=XAppTokenAuth, settings=current_dir + '/../config/settings.py')

    hook_up_callbacks(app)
    register_apps(app)
    return app

# Hook up additional Flask controllers
def register_apps(app):
    app.register_blueprint(auth)

def hook_up_callbacks(app):
    app.on_post_GET_client_apps += process_client_app_token
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

def normalize_user(users):
  for user in users:
    # encrypt password
    user['password'] = bcrypt.hashpw(user['password'], bcrypt.gensalt())
    # normalize email
    user['email'] = user['email'].lower()
    # TODO link social account
