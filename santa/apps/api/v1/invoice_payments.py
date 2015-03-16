# -*- coding: utf-8 -*-

from flask import Blueprint, request
from santa.lib.api_errors import ApiException
from santa.models.domain import *
from santa.lib.common import parse_request, render_json, me_to_json
from santa.lib.auth import require_app_auth
from santa.apps.api.util.paginate import paginate
from santa.apps.api.util.sort import sort
from mongoengine import *

invoice_payments = Blueprint('invoice_payments', __name__)

@invoice_payments.route('/invoice_payments', methods=['GET'])
@require_app_auth
def get_invoice_payments():
    paginated_and_sorted = paginate(sort(InvoicePayment.objects, request.args), request.args)

    return render_json(me_to_json(paginated_and_sorted))

@invoice_payments.route('/invoice_payments/<invoice_payment_id>', methods=['GET'])
@require_app_auth
def get_invoice_payment(invoice_payment_id):
    invoice_payment = InvoicePayment.objects(id=invoice_payment_id).first()

    if not invoice_payment:
        raise ApiException('invoice payment not found', 404)

    return render_json(me_to_json(invoice_payment))

@invoice_payments.route('/invoice_payments', methods=['POST'])
@require_app_auth
def create_invoice_payment():
    data = parse_request(request)

    new_invoice_payment = InvoicePayment(**{ k: v for (k, v) in data.iteritems() if k in InvoicePayment._fields.keys() })

    new_invoice_payment.save()

    return render_json(me_to_json(new_invoice_payment), status=201)

@invoice_payments.route('/invoice_payments/<invoice_payment_id>', methods=['PUT'])
@require_app_auth
def update_invoice_payment(invoice_payment_id):
    data = parse_request(request)

    invoice_payment = InvoicePayment.objects(id=invoice_payment_id).first()
    if not invoice_payment:
        raise ApiException('invoice payment not found', 404)

    # QuerySet update() or Document modify() does not validate, so we use
    # save() here.
    # http://docs.mongoengine.org/en/latest/apireference.html#mongoengine.queryset.QuerySet.update
    # http://docs.mongoengine.org/en/latest/apireference.html#mongoengine.Document.modify
    # https://github.com/MongoEngine/mongoengine/issues/453

    # The setattr() approach has to use the class instances to assign
    # ReferenceField or EmbeddedField; however, save(), like creation, can
    # accept raw data, e.g. string for ObjectId, and dict for embedd field.

    # If the document already exists, save() will update the existing one.
    # http://docs.mongoengine.org/en/latest/apireference.html#mongoengine.Document.save
    data['id'] = invoice_payment_id
    invoice_payment = InvoicePayment(**{ k: v for (k, v) in data.iteritems() if k in InvoicePayment._fields.keys() })
    invoice_payment.save()

    return render_json(me_to_json(invoice_payment))

@invoice_payments.route('/invoice_payments/<invoice_payment_id>', methods=['DELETE'])
@require_app_auth
def delete_invoice_payment(invoice_payment_id):
    invoice_payment = InvoicePayment.objects(id=invoice_payment_id).first()

    if not invoice_payment:
        raise ApiException('invoice payment not found', 404)

    invoice_payment.delete()

    return render_json(me_to_json(invoice_payment))
