# -*- coding: utf-8 -*-
"""
    settings.staging.py.example
    ~~~~~~~~~~~~~~~

    An example of staging settings that *override*
    default settings in settings.py.
"""
#
# Flask configuration
#

DEBUG = False

#
# Custom Flask app configuration
#

#
# Database configuration
#

MONGO_HOST      = 'localhost'
MONGO_PORT      = 27017
MONGO_USERNAME  = ''
MONGO_PASSWORD  = ''
MONGO_DBNAME    = ''

#
# Customized configuration
#

TOKEN_TRUST_KEY   = ''
MANDRILL_API_KEY  = ''
