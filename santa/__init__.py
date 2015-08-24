import os, re, json
from flask import jsonify, Flask
from flask.ext.cors import CORS
from santa.lib.api_errors import ApiException
from mongoengine import connect
from mongoengine.errors import *

def create_app():
    app = Flask(__name__)
    # Load configs from the default settings file.
    app.config.from_object('santa.config.settings')

    # Override configs from the env specified in the SANTA_ENV env var.
    if 'SANTA_ENV' in os.environ and os.environ['SANTA_ENV'] != 'development':
        app.config.from_object('santa.config.settings_' + os.environ['SANTA_ENV'])

    # Override configs directly from env vars. Convert types by parsing as JSON.
    # Note that all the configs provided in the env vars have to namespace with
    # `SANTA_` prefix, e.g. HOST becomes SANTA_HOST.
    for key, value in os.environ.iteritems():
        match = re.search(r'^SANTA_(.*)', key)
        c = match and match.group(1)
        if c in app.config:
            try:
                app.config[c] = json.loads(value)
            except ValueError:
                app.config[c] = value

    CORS(app)

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
            # TODO: Transform error messages to be more informative
            # e.g. A NotUniqueError might give a "Tried to save duplicate unique keys (E11000 duplicate key error index: santa-test.users.$email_1  dup key: { : \\"takochan@takoman.co\\" })" message
            error = ApiException(str(error))
        elif isinstance(error, ValidationError):
            # TODO: Transform error messages to be more informative
            # e.g. A ValidationError might give a "Only lists and tuples may be used in a list field: [\'role\']" message
            message = error._format_errors() or error.message or 'unknown error'
            error = ApiException(message)
        elif isinstance(error, ApiException):
            pass
        else:
            error = ApiException(str(error))

        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

# Register Flask blueprints
def register_apps(app):
    # System wide apps
    from apps.site.controllers import site
    from apps.auth.controllers import auth
    app.register_blueprint(site)
    app.register_blueprint(auth)

    # API v1 endpoints
    from apps.api.v1 import endpoints
    for endpoint in endpoints:
        app.register_blueprint(endpoint, url_prefix='/api/v1')

    # API v2 endpoints
    from apps.api.v2 import endpoints
    for endpoint in endpoints:
        app.register_blueprint(endpoint, url_prefix='/api/v2')
