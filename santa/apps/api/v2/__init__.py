# -*- coding: utf-8 -*-

import orders

endpoints = map(lambda module: module.app, (orders,))
