# -*- coding: utf-8 -*-

from flask import Blueprint, request
from santa.lib.api_errors import ApiException
from santa.models.domain import *
from santa.lib.common import parse_request, render_json, me_to_json
from santa.lib.auth import require_app_auth
from santa.apps.api.util.paginate import paginate
from santa.apps.api.util.sort import sort
from mongoengine import *

invoices = Blueprint('invoices', __name__)

@invoices.route('/invoices', methods=['GET'])
@require_app_auth
def get_invoices():
    paginated_and_sorted = paginate(sort(Invoice.objects, request.args), request.args)

    return render_json(me_to_json(paginated_and_sorted))

@invoices.route('/invoices/<invoice_id>', methods=['GET'])
@require_app_auth
def get_invoice(invoice_id):
    invoice = Invoice.objects(id=invoice_id).first()

    if not invoice:
        raise ApiException('invoice not found', 404)

    return render_json(me_to_json(invoice))

@invoices.route('/invoices', methods=['POST'])
@require_app_auth
def create_invoice():
    data = parse_request(request)

    new_invoice = Invoice(**{ k: v for (k, v) in data.iteritems() if k in Invoice._fields.keys() })

    new_invoice.save()

    return render_json(me_to_json(new_invoice), status=201)

@invoices.route('/invoices/<invoice_id>', methods=['PUT'])
@require_app_auth
def update_invoice(invoice_id):
    data = parse_request(request)

    invoice = Invoice.objects(id=invoice_id).first()
    if not invoice:
        raise ApiException('invoice not found', 404)

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
    data['id'] = invoice_id
    invoice = Invoice(**{ k: v for (k, v) in data.iteritems() if k in Invoice._fields.keys() })
    invoice.save()

    return render_json(me_to_json(invoice))

@invoices.route('/invoices/<invoice_id>', methods=['DELETE'])
@require_app_auth
def delete_invoice(invoice_id):
    invoice = Invoice.objects(id=invoice_id).first()

    if not invoice:
        raise ApiException('invoice not found', 404)

    invoice.delete()

    return render_json(me_to_json(invoice))