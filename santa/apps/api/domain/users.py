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
        'name': {
            'type'      : 'string',
            'maxlength' : 256,
            'required'  : True,
            'empty'     : False
        },
        'email': {
            'type'      : 'string',
            'maxlength' : 256,
            # Consider using custom validators for more readable error messages
            'regex'     : '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'required'  : True,
            'unique'    : True,
            'empty'     : False
        },
        'password': {
            'type'      : 'string',
            'minlength' : 8,
            'required'  : True
        },
        'role': {
            'type'      : 'list',
            'allowed'   : ["user", "takoman", "admin"]
        },
    }
}
