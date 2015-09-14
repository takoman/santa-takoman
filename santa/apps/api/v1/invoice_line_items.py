# -*- coding: utf-8 -*-

from flask import Blueprint, request
from santa.lib.api_errors import ApiException
from santa.models.domain import *
from santa.lib.common import parse_request, render_json, me_to_json
from santa.lib.auth import require_app_auth
from santa.apps.api.util.paginate import paginate
from santa.apps.api.util.sort import sort
from mongoengine import *

app = Blueprint('v1.invoice_line_items', __name__)

@app.route('/invoice_line_items', methods=['GET'])
@require_app_auth
def get_invoice_line_items():
    invoice_id = request.args.get('invoice_id', None)
    if not invoice_id:
        raise ApiException('missing invoice id', 404)

    invoice = Invoice.objects(id=invoice_id).first()
    if not invoice:
        raise ApiException('invoice not found', 404)

    paginated_and_sorted = paginate(sort(
        InvoiceLineItem.objects(invoice=invoice), request.args), request.args)

    return render_json(me_to_json(paginated_and_sorted))

@app.route('/invoice_line_items/<invoice_line_item_id>', methods=['GET'])
@require_app_auth
def get_invoice_line_item(invoice_line_item_id):
    item = InvoiceLineItem.objects(id=invoice_line_item_id).first()

    if not item:
        raise ApiException('invoice line item not found', 404)

    return render_json(me_to_json(item))

@app.route('/invoice_line_items', methods=['POST'])
@require_app_auth
def create_invoice_line_item():
    data = parse_request(request)

    invoice_id = data.get('invoice')
    order_line_item_id = data.get('order_line_item')

    if not invoice_id:
        raise ApiException('missing invoice id', 404)

    invoice = Invoice.objects(id=invoice_id).first()

    if not invoice:
        raise ApiException('invoice not found', 404)

    if not order_line_item_id:
        raise ApiException('missing order line item id', 404)

    order_line_item = OrderLineItem.objects(id=order_line_item_id).first()

    if not order_line_item:
        raise ApiException('order line item not found', 404)

    # TODO: easier way to compare two documents?
    if not str(invoice.order.id) == str(order_line_item.order.id):
        raise ApiException('order line item and invoice associated with different order', 400)

    new_item = InvoiceLineItem(**{ k: v for (k, v) in data.iteritems() if k in InvoiceLineItem._fields.keys() })

    new_item.save()

    return render_json(me_to_json(new_item), status=201)

@app.route('/invoice_line_items/<invoice_line_item_id>', methods=['PUT'])
@require_app_auth
def update_invoice_line_item(invoice_line_item_id):
    data = parse_request(request)

    invoice_line_item = InvoiceLineItem.objects(id=invoice_line_item_id).first()
    if not invoice_line_item:
        raise ApiException('invoice line item not found', 404)

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
    data['id'] = invoice_line_item_id
    invoice_line_item = InvoiceLineItem(**{ k: v for (k, v) in data.iteritems() if k in InvoiceLineItem._fields.keys() })
    invoice_line_item.save()

    return render_json(me_to_json(invoice_line_item))

@app.route('/invoice_line_items/<invoice_line_item_id>', methods=['DELETE'])
@require_app_auth
def delete_invoice_line_item(invoice_line_item_id):
    invoice_line_item = InvoiceLineItem.objects(id=invoice_line_item_id).first()

    if not invoice_line_item:
        raise ApiException('invoice line item not found', 404)

    invoice_line_item.delete()

    return render_json(me_to_json(invoice_line_item))
