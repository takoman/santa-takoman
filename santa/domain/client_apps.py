# -*- coding: utf-8 -*-
"""
  santa.domain.client_apps.py
  ~~~~~~~~~~~~~~~~~~~~~~~

  'client_apps' resource and schema settings.

  :copyright: (c) 2013 by Chung-Yi Chi
  :license:
"""

# This resource is used as an item, it must be passed with client_id and
# client_secret in request arguments and will return the token, see
# `process_client_app_token()` function for details.
definition = {
  'url': 'xapp_token',
  'datasource': { 'source': 'client_apps' },

  'public_methods': ['GET'],
  'public_item_methods': [],

  # We also disable endpoint caching as we don't want client apps to
  # cache app data.
  'cache_control': '',
  'cache_expires': 0,

  'datasource': {
    'projection': {'token': 1}
  },
  'schema': {
    'client_id': {
      'type': 'string',
      'minlength': 8,
      'required': True
    },
    'client_secret': {
      'type': 'string',
      'minlength': 8,
      'required': True
    },
    'token': {
      'type': 'string',
      'minlength': 8,
      'required': True
    }
  }
}
