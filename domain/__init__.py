# -*- coding: utf-8 -*-
"""
  santa.domain
  ~~~~~~~~~~~

  this package exposes the API domain.

  :copyright: (c) 2014 by Chung-Yi Chi
  :license: 
"""
import client_apps, users

DOMAIN = {
  'client_apps': client_apps.definition,
  'users': users.definition
}
