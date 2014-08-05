# -*- coding: utf-8 -*-
"""
    santa.domain.social_authentications.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    'social_authentications' resource and schema settings.

    :copyright: (c) 2014 by Chung-Yi Chi
    :license:
"""

definition = {
    # 'allowed_roles': ['admin'],
    # 'authentication': BCryptAuth(),

    # We also disable endpoint caching as we don't want client apps to
    # cache account data.
    'cache_control': '',
    'cache_expires': 0,

    'schema': {
        # always required
        'uid': {
            'type'      : 'string',
            'required'  : True
        },
        'user': {
            'type'      : 'objectid',
            'required'  : True,
            'data_relation': {
                'resource'  : 'users',
                'field'     : '_id',
                'embeddable': True
            }
        },
        # sometimes supplied, depending on the provider
        'name': {
            'type'      : 'string',
            'maxlength' : 256
        },
        'email': {
            'type'      : 'string',
            'maxlength' : 256,
            'regex'     : '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        },
        'first_name': {
            'type'      : 'string',
            'maxlength' : 256
        },
        'last_name': {
            'type'      : 'string',
            'maxlength' : 256
        },
        'nickname'      : {'type': 'string'},
        'location'      : {'type': 'string'},
        'description'   : {'type': 'string'},
        'image'         : {'type': 'string'},
        'phone'         : {'type': 'string'},
        'urls'          : {'type': 'dict'},
        'credentials'   : {'type': 'dict'},
        'extra'         : {'type': 'dict'}
    }
}
