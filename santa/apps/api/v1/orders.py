# -*- coding: utf-8 -*-

from flask import Blueprint, request
from santa.lib.api_errors import ApiException
from santa.models.domain import *
from santa.lib.common import parse_request, render_json, me_to_json
from santa.lib.auth import require_app_auth
from santa.apps.api.util.paginate import paginate
from santa.apps.api.util.sort import sort
from mongoengine import *

orders = Blueprint('orders', __name__)

@orders.route('/orders', methods=['GET'])
@require_app_auth
def get_orders():
    paginated_and_sorted = paginate(sort(Order.objects, request.args), request.args)

    return render_json(me_to_json(paginated_and_sorted))

@orders.route('/orders/<order_id>', methods=['GET'])
@require_app_auth
def get_order(order_id):
    order = Order.objects(id=order_id).first()

    if not order:
        raise ApiException('order not found', 404)

    return render_json(me_to_json(order))

@orders.route('/orders', methods=['POST'])
@require_app_auth
def create_order():
    data = parse_request(request)

    new_order = Order(**{ k: v for (k, v) in data.iteritems() if k in Order._fields.keys() })

    new_order.save()

    return render_json(me_to_json(new_order), status=201)

@orders.route('/orders/<order_id>', methods=['PUT'])
@require_app_auth
def update_order(order_id):
    data = parse_request(request)

    known_fields = Order._fields.keys()
    order = Order.objects(id=order_id).first()
    if not order:
        raise ApiException('order not found', 404)

    for k, v in data.iteritems():
        if k in known_fields:
            if (isinstance(Order._fields[k], ReferenceField)):
                v = Order._fields[k].document_type.objects(id=v).first()
                if not v:
                    raise ApiException(k + ' not found')
            setattr(order, k, v)
    order.save()

    return render_json(me_to_json(order))

@orders.route('/orders/<order_id>', methods=['DELETE'])
@require_app_auth
def delete_order(order_id):
    order = Order.objects(id=order_id).first()

    if not order:
        raise ApiException('order not found', 404)

    order.delete()

    return render_json(me_to_json(order))
