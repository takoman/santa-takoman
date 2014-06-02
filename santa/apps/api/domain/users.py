# -*- coding: utf-8 -*-
"""
    santa.domain.users.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    'users' resource and schema settings.

    :copyright: (c) 2013 by Chung-Yi Chi
    :license:
"""

definition = {
    # 'allowed_roles': ['admin'],
    # 'authentication': BCryptAuth(),

    # the standard account entry point is defined as
    # '/users/<ObjectId>'. We define  an additional read-only entry
    # point accessible at '/accounts/<username>'.
    # 'additional_lookup': {
    #     'url': 'regex("[\w-]+")',
    #     'field': 'name',
    # },

    # We also disable endpoint caching as we don't want client apps to
    # cache account data.
    'cache_control': '',
    'cache_expires': 0,

    'datasource': {
        'projection': {'password': 0}
    },
    'schema': {
        '_id': {
            'type'      : 'string'
        },
        'name': {
            'type'      : 'string',
            'maxlength' : 256,
        },
        'email': {
            'type'      : 'string',
            'maxlength' : 256,
            # Consider using custom validators for more readable error messages
            'regex'     : '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        },
        'password': {
            'type'      : 'string',
            'minlength' : 8,
        },
        # oauth_token and provider fields here are only for avoiding unknown
        # fields error when social signups. We will remove them when inserting
        # to database. See more:
        # http://python-eve.org/validation.html#allowing-the-unknown
        'oauth_token': {
            'type'      : 'string'
        },
        'provider': {
            'type'      : 'string'
        },
        'role': {
            'type'      : 'list',
            'allowed'   : ["user", "takoman", "admin"]
        },
    }
}
