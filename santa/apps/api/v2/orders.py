# -*- coding: utf-8 -*-

from flask import g, Blueprint
from santa.lib.api_errors import ApiException
from santa.models.domain import *
from santa.lib.common import render_json, me_to_json
from santa.lib.auth import require_user_auth
from mongoengine import *

app = Blueprint('v2.orders', __name__)

@app.route('/orders/<order_id>', methods=['GET'])
@require_user_auth
def get_order(order_id):
    order = Order.objects(id=order_id).first()

    if not order:
        raise ApiException('order not found', 404)

    if g.user.id not in map(lambda u: u and u.id, [order.merchant.user, order.customer]):
        raise ApiException('user not authorized to access the order', 400)

    return render_json(me_to_json(order))
