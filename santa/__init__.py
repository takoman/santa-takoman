import os, re
from flask import jsonify, Flask
from santa.lib.api_errors import ApiException
from mongoengine import connect
from mongoengine.errors import *

def create_app():
    app = Flask(__name__)
    # Load configs from the default settings file.
    app.config.from_object('santa.config.settings')

    # Override configs from the file specified in the SANTA_SETTINGS env var.
    if 'SANTA_SETTINGS' in os.environ:
        app.config.from_envvar('SANTA_SETTINGS')

    # Override configs directly from env vars. Convert types. Note that all the
    # configs provided in the env vars have to namespace with `SANTA_` prefix.
    # E.g. HOST becomes SANTA_HOST.
    for key, value in os.environ.iteritems():
        match = re.search(r'^SANTA_(.*)', key)
        c = match and match.group(1)
        if c in app.config:
            app.config[c] = type(app.config[c])(value)

    app.db = connect_db(app)
    hook_up_error_handlers(app)
    register_apps(app)
    return app

def connect_db(app):
    return connect(app.config['MONGO_DBNAME'],
                   host=app.config['MONGO_HOST'],
                   port=app.config['MONGO_PORT'])

def hook_up_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_api_exception(error):
        if any(map(lambda e: isinstance(error, e), [
            NotRegistered, InvalidDocumentError, LookUpError, DoesNotExist,
            MultipleObjectsReturned, InvalidQueryError, OperationError,
            NotUniqueError])):

            # TODO: Categorize these with different status_code
            error = ApiException(str(error))
        elif isinstance(error, ValidationError):
            error = ApiException(error._format_errors())
        elif isinstance(error, ApiException):
            pass
        else:
            error = ApiException(str(error))

        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

# Hook up Flask blueprints
def register_apps(app):
    from apps.site.controllers import site
    from apps.api.v1.users import users
    from apps.api.v1.client_apps import client_apps
    from apps.api.v1.me import me
    from apps.api.v1.system import system
    from apps.auth.controllers import auth
    app.register_blueprint(site)
    app.register_blueprint(auth)
    app.register_blueprint(me, url_prefix='/api/v1')
    app.register_blueprint(users, url_prefix='/api/v1')
    app.register_blueprint(client_apps, url_prefix='/api/v1')
    app.register_blueprint(system, url_prefix='/api/v1')
