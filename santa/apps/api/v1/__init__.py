# -*- coding: utf-8 -*-

import users
import merchants
import products
import orders
import order_line_items
import invoices
import invoice_line_items
import invoice_payments
import payment_accounts
import client_apps
import me
import system

endpoints = map(lambda module: module.app, (users,
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
                                            system))
