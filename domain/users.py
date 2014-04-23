# -*- coding: utf-8 -*-
"""
  santa.domain.users.py
  ~~~~~~~~~~~~~~~~~~~~~~~

  'users' resource and schema settings.

  :copyright: (c) 2013 by Chung-Yi Chi
  :license:
"""

from auth import BCryptAuth

definition = {
  #'allowed_roles': ['admin'],
  'authentication': BCryptAuth(),

  # the standard account entry point is defined as
  # '/users/<ObjectId>'. We define  an additional read-only entry
  # point accessible at '/accounts/<username>'.
  'additional_lookup': {
    'url': 'regex("[\w-]+")',
    'field': 'username',
  },

  # We also disable endpoint caching as we don't want client apps to
  # cache account data.
  'cache_control': '',
  'cache_expires': 0,

  'datasource': {
    'projection': {'password': 0}
  },
  'schema': {
    'username': {
      'type': 'string',
      'minlength': 1
    },
    'password': {
      'type': 'string',
      'minlength': 8
    },
    'role': {
      'type': 'list',
      'allowed': ["user", "admin"]
    },
  }
}
