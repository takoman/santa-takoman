# -*- coding: utf-8 -*-
"""
    settings.py
    ~~~~~~~~~~~

    Default settings for the development environment.

    Settings for different environments should *override* the settings here.
    Settings for the production environment.
    The settings defined here will *override* the default settings.
    * This file should only define Flask built-in configurations
    (http://flask.pocoo.org/docs/0.10/config/#builtin-configuration-values).
    For custom and third-party service configurations, we follow the 12-factor
    apps and define those values in the environment variables.
"""
#
# Flask configuration
#

# APPLICATION_ROOT              = None
DEBUG                           = True
# JSON_AS_ASCII                 = True
# JSON_SORT_KEYS                = True
# JSONIFY_PRETTYPRINT_REGULAR   = True
# LOGGER_NAME                   = None
# MAX_CONTENT_LENGTH            = None
# PERMANENT_SESSION_LIFETIME    = datetime.timedelta(31)
# PREFERRED_URL_SCHEME          = 'http'
# PRESERVE_CONTEXT_ON_EXCEPTION = None
# PROPAGATE_EXCEPTIONS          = None
# SECRET_KEY                    = None
# SEND_FILE_MAX_AGE_DEFAULT     = 43200
# SERVER_NAME                   = None
# SESSION_COOKIE_DOMAIN         = None
# SESSION_COOKIE_HTTPONLY       = True
# SESSION_COOKIE_NAME           = 'session'
# SESSION_COOKIE_PATH           = None
# SESSION_COOKIE_SECURE         = False
# TESTING                       = False
# TRAP_BAD_REQUEST_ERRORS       = False
# TRAP_HTTP_EXCEPTIONS          = False
# USE_X_SENDFILE                = False

#
# Custom Flask app configuration
#
HOST = '127.0.0.1'
PORT = 5000
ENV  = 'development'

#
# Database configuration
#
MONGO_HOST     = 'localhost'
MONGO_PORT     = 27017
MONGO_DBNAME   = 'santa-local'
MONGO_USERNAME = None
MONGO_PASSWORD = None

#
# Flask-Cors
#
CORS_ALLOW_HEADERS = ['Content-Type', 'X-XAPP-TOKEN']
CORS_RESOURCES = {r"/api/*": {"origins": "*"}}

# Be sure to restart your server when you modify this file.
# Your secret key for verifying the integrity of signed cookies.
# If you change this key, all old signed cookies will become invalid!
# Make sure the secret is at least 30 characters and all random,
# no regular words or you'll be exposed to dictionary attacks.
TOKEN_TRUST_KEY = '33578d92d919ca4aaaec930ee4d3d5df754f057e61e93a2247ab7fe13d712ff4072aa6c327601b7009d5bf998f9c70795c1f81ae25f48cfc4607f6c2cc765b48'

MANDRILL_API_KEY = None
NEW_RELIC_CONFIG_FILE = 'newrelic.ini'
NEW_RELIC_ENVIRONMENT = 'development'
