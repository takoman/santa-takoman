# -*- coding: utf-8 -*-

from flask import Blueprint, request
from santa.lib.api_errors import ApiException
from santa.models.domain import *
from santa.lib.common import parse_request, render_json, me_to_json
from santa.lib.auth import require_app_auth
from santa.apps.api.util.paginate import paginate
from santa.apps.api.util.sort import sort
from mongoengine import *

order_line_items = Blueprint('order_line_items', __name__)

@order_line_items.route('/order_line_items', methods=['GET'])
@require_app_auth
def get_order_line_items():
    order_id = request.args.get('order_id', None)
    if not order_id:
        raise ApiException('missing order_id param', 404)

    order = Order.objects(id=order_id).first()
    if not order:
        raise ApiException('order not found', 404)

    paginated_and_sorted = paginate(sort(
        OrderLineItem.objects(order=order), request.args), request.args)

    return render_json(me_to_json(paginated_and_sorted))
