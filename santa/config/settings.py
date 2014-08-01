# -*- coding: utf-8 -*-
"""
    settings.py
    ~~~~~~~~~~~~~~~

    Default settings for development.
    Settings for different environments should *override* the settings here.
"""
#
# Flask configuration
#

DEBUG       = True
# SERVER_NAME = '127.0.0.1:5000'

#
# Custom Flask app configuration
#

HOST = '127.0.0.1'
PORT = 5000

#
# Database configuration
#

MONGO_HOST      = 'localhost'
MONGO_PORT      = 27017
# MONGO_USERNAME  = ''
# MONGO_PASSWORD  = ''
MONGO_DBNAME    = 'santa-local'

#
# Customized configuration
#

# Be sure to restart your server when you modify this file.
# Your secret key for verifying the integrity of signed cookies.
# If you change this key, all old signed cookies will become invalid!
# Make sure the secret is at least 30 characters and all random,
# no regular words or you'll be exposed to dictionary attacks.
TOKEN_TRUST_KEY     = '33578d92d919ca4aaaec930ee4d3d5df754f057e61e93a2247ab7fe13d712ff4072aa6c327601b7009d5bf998f9c70795c1f81ae25f48cfc4607f6c2cc765b48'

MANDRILL_API_KEY    = 'THdzAyk7NFSJmH4Qn04cOQ'
