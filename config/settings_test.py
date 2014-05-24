# -*- coding: utf-8 -*-
"""
    settings.test.py
    ~~~~~~~~~~~~~~~

    An example of test settings that *override*
    default settings in settings.py.
"""

DEBUG = True

# Running on local machine. Let's just use the local mongod instance.
MONGO_HOST      = 'localhost'
MONGO_PORT      = 27017
MONGO_USERNAME  = ''
MONGO_PASSWORD  = ''
MONGO_DBNAME    = 'test-database'

# let's not forget the API entry point (not really needed anyway)
# SERVER_NAME = '127.0.0.1:5000'

# HATEOAS
# HATEOAS = False

# CORS
# X_DOMAINS = '*'
# X_HEADERS = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'

# JSON and/or XML
# XML = False

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
# RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
# ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
# CACHE_CONTROL = 'max-age=20'
# CACHE_EXPIRES = 20

# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
# DOMAIN = domain.DOMAIN
