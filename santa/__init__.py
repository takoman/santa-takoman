import os
from flask import jsonify, Flask
from santa.lib.api_errors import ApiException
from mongoengine import connect

def create_app():
    app = Flask(__name__)
    app.config.from_object('santa.config.settings')
    if 'SANTA_SETTINGS' in os.environ:
        app.config.from_envvar('SANTA_SETTINGS')

    connect_db(app)
    hook_up_error_handlers(app)
    register_apps(app)
    return app

def connect_db(app):
    connect(app.config['MONGO_DBNAME'],
            host=app.config['MONGO_HOST'],
            port=app.config['MONGO_PORT'])

def hook_up_error_handlers(app):
    @app.errorhandler(ApiException)
    def handle_api_oauth_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

# Hook up Flask blueprints
def register_apps(app):
    from apps.api.domain.users import users
    from apps.api.domain.client_apps import client_apps
    from apps.auth.controllers import auth
    from apps.me.controllers import me
    app.register_blueprint(auth)
    app.register_blueprint(me)
    app.register_blueprint(users)
    app.register_blueprint(client_apps)
