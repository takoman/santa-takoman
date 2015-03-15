import os, re
from flask import jsonify, Flask
from flask.ext.cors import CORS
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

# Hook up Flask blueprints
def register_apps(app):
    from apps.site.controllers import site
    from apps.api.v1.users import users
    from apps.api.v1.merchants import merchants
    from apps.api.v1.products import products
    from apps.api.v1.orders import orders
    from apps.api.v1.order_line_items import order_line_items
    from apps.api.v1.invoices import invoices
    from apps.api.v1.order_payments import order_payments
    from apps.api.v1.payment_accounts import payment_accounts
    from apps.api.v1.client_apps import client_apps
    from apps.api.v1.me import me
    from apps.api.v1.system import system
    from apps.auth.controllers import auth
    app.register_blueprint(site)
    app.register_blueprint(auth)
    app.register_blueprint(me, url_prefix='/api/v1')
    app.register_blueprint(users, url_prefix='/api/v1')
    app.register_blueprint(merchants, url_prefix='/api/v1')
    app.register_blueprint(products, url_prefix='/api/v1')
    app.register_blueprint(orders, url_prefix='/api/v1')
    app.register_blueprint(order_line_items, url_prefix='/api/v1')
    app.register_blueprint(invoices, url_prefix='/api/v1')
    app.register_blueprint(order_payments, url_prefix='/api/v1')
    app.register_blueprint(payment_accounts, url_prefix='/api/v1')
    app.register_blueprint(client_apps, url_prefix='/api/v1')
    app.register_blueprint(system, url_prefix='/api/v1')
