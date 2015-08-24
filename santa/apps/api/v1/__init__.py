# -*- coding: utf-8 -*-

from santa.apps.api.v1.users import users
from santa.apps.api.v1.merchants import merchants
from santa.apps.api.v1.products import products
from santa.apps.api.v1.orders import orders
from santa.apps.api.v1.order_line_items import order_line_items
from santa.apps.api.v1.invoices import invoices
from santa.apps.api.v1.invoice_line_items import invoice_line_items
from santa.apps.api.v1.invoice_payments import invoice_payments
from santa.apps.api.v1.payment_accounts import payment_accounts
from santa.apps.api.v1.client_apps import client_apps
from santa.apps.api.v1.me import me
from santa.apps.api.v1.system import system

endpoints = (users,
             merchants,
             products,
             orders,
             order_line_items,
             invoices,
             invoice_line_items,
             invoice_payments,
             payment_accounts,
             client_apps,
             me,
             system)
