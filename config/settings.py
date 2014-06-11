from santa.apps.api import domain

DEBUG = True

# Running on local machine. Let's just use the local mongod instance.
MONGO_HOST      = 'localhost'
MONGO_PORT      = 27017
# MONGO_USERNAME  = ''
# MONGO_PASSWORD  = ''
MONGO_DBNAME    = 'santa_local'

# let's not forget the API entry point (not really needed anyway)
# SERVER_NAME     = '127.0.0.1:5000'
URL_PREFIX      = 'api'
API_VERSION     = 'v1'

# HATEOAS
HATEOAS = False

# Data validation error messages
STATUS = 'status'
ISSUES = 'message'
STATUS_OK = 'success'
STATUS_ERR = 'error'

# CORS
X_DOMAINS = '*'
X_HEADERS = 'Origin, X-Requested-With, Content-Type, Accept, Authorization, X-XAPP-TOKEN'

# JSON and/or XML
XML = False

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = domain.DOMAIN

#
# Customized configuration
#

# Be sure to restart your server when you modify this file.
# Your secret key for verifying the integrity of signed cookies.
# If you change this key, all old signed cookies will become invalid!
# Make sure the secret is at least 30 characters and all random,
# no regular words or you'll be exposed to dictionary attacks.
TOKEN_TRUST_KEY = '33578d92d919ca4aaaec930ee4d3d5df754f057e61e93a2247ab7fe13d712ff4072aa6c327601b7009d5bf998f9c70795c1f81ae25f48cfc4607f6c2cc765b48'

MANDRILL_API_KEY = 'THdzAyk7NFSJmH4Qn04cOQ'
