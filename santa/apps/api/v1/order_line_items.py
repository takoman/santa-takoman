# -*- coding: utf-8 -*-

from flask import Blueprint, request
from santa.lib.api_errors import ApiException
from santa.models.domain import *
from santa.lib.common import parse_request, render_json, me_to_json
from santa.lib.auth import require_app_auth
from santa.apps.api.util.paginate import paginate
from santa.apps.api.util.sort import sort
from mongoengine import *

app = Blueprint('v1.order_line_items', __name__)

@app.route('/order_line_items', methods=['GET'])
@require_app_auth
def get_order_line_items():
    order_id = request.args.get('order_id', None)
    if not order_id:
        raise ApiException('missing order id', 404)

    order = Order.objects(id=order_id).first()
    if not order:
        raise ApiException('order not found', 404)

    paginated_and_sorted = paginate(sort(
        OrderLineItem.objects(order=order), request.args), request.args)

    return render_json(me_to_json(paginated_and_sorted))

@app.route('/order_line_items/<order_line_item_id>', methods=['GET'])
@require_app_auth
def get_order_line_item(order_line_item_id):
    item = OrderLineItem.objects(id=order_line_item_id).first()

    if not item:
        raise ApiException('order line item not found', 404)

    return render_json(me_to_json(item))

@app.route('/order_line_items', methods=['POST'])
@require_app_auth
def create_order_line_item():
    data = parse_request(request)

    order_id = data.get('order')
    product_id = data.get('product')

    if not order_id:
        raise ApiException('missing order id', 404)

    if not Order.objects(id=order_id).first():
        raise ApiException('order not found', 404)

    if product_id and not Product.objects(id=product_id).first():
        raise ApiException('product not found', 404)

    new_item = OrderLineItem(**{ k: v for (k, v) in data.iteritems() if k in OrderLineItem._fields.keys() })

    new_item.save()

    return render_json(me_to_json(new_item), status=201)

@app.route('/order_line_items/<order_line_item_id>', methods=['PUT'])
@require_app_auth
def update_order_line_item(order_line_item_id):
    data = parse_request(request)

    known_fields = OrderLineItem._fields.keys()
    order_line_item = OrderLineItem.objects(id=order_line_item_id).first()
    if not order_line_item:
        raise ApiException('order line item not found', 404)

    for k, v in data.iteritems():
        if k in known_fields:
            if (isinstance(OrderLineItem._fields[k], ReferenceField)):
                v = OrderLineItem._fields[k].document_type.objects(id=v).first()
                if not v:
                    raise ApiException(k + ' not found')
            setattr(order_line_item, k, v)
    order_line_item.save()

    return render_json(me_to_json(order_line_item))

@app.route('/order_line_items/<order_line_item_id>', methods=['DELETE'])
@require_app_auth
def delete_order_line_item(order_line_item_id):
    order_line_item = OrderLineItem.objects(id=order_line_item_id).first()

    if not order_line_item:
        raise ApiException('order line item not found', 404)

    order_line_item.delete()

    return render_json(me_to_json(order_line_item))
