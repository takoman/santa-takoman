# -*- coding: utf-8 -*-

from flask import Blueprint, request
from santa.lib.api_errors import ApiException
from santa.models.domain import *
from santa.lib.common import parse_request, render_json, me_to_json
from santa.lib.auth import require_app_auth
from santa.apps.api.util.paginate import paginate
from santa.apps.api.util.sort import sort
from mongoengine import *

order_payments = Blueprint('order_payments', __name__)

@order_payments.route('/order_payments', methods=['GET'])
@require_app_auth
def get_order_payments():
    paginated_and_sorted = paginate(sort(OrderPayment.objects, request.args), request.args)

    return render_json(me_to_json(paginated_and_sorted))

@order_payments.route('/order_payments/<order_payment_id>', methods=['GET'])
@require_app_auth
def get_order_payment(order_payment_id):
    order_payment = OrderPayment.objects(id=order_payment_id).first()

    if not order_payment:
        raise ApiException('order payment not found', 404)

    return render_json(me_to_json(order_payment))

@order_payments.route('/order_payments', methods=['POST'])
@require_app_auth
def create_order_payment():
    data = parse_request(request)

    new_order_payment = OrderPayment(**{ k: v for (k, v) in data.iteritems() if k in OrderPayment._fields.keys() })

    new_order_payment.save()

    return render_json(me_to_json(new_order_payment), status=201)

@order_payments.route('/order_payments/<order_payment_id>', methods=['PUT'])
@require_app_auth
def update_order_payment(order_payment_id):
    data = parse_request(request)

    order_payment = OrderPayment.objects(id=order_payment_id).first()
    if not order_payment:
        raise ApiException('order payment not found', 404)

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
    data['id'] = order_payment_id
    order_payment = OrderPayment(**{ k: v for (k, v) in data.iteritems() if k in OrderPayment._fields.keys() })
    order_payment.save()

    return render_json(me_to_json(order_payment))

@order_payments.route('/order_payments/<order_payment_id>', methods=['DELETE'])
@require_app_auth
def delete_order_payment(order_payment_id):
    order_payment = OrderPayment.objects(id=order_payment_id).first()

    if not order_payment:
        raise ApiException('order payment not found', 404)

    order_payment.delete()

    return render_json(me_to_json(order_payment))
