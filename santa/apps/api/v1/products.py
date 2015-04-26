# -*- coding: utf-8 -*-

from flask import Blueprint, request
from santa.lib.api_errors import ApiException
from santa.models.domain import *
from santa.lib.common import parse_request, render_json, me_to_json
from santa.lib.auth import require_app_auth
from santa.apps.api.util.paginate import paginate
from santa.apps.api.util.sort import sort

products = Blueprint('products', __name__)

@products.route('/products', methods=['GET'])
@require_app_auth
def get_products():
    paginated_and_sorted = paginate(sort(Product.objects, request.args), request.args)

    return render_json(me_to_json(paginated_and_sorted))

@products.route('/products/<product_id>', methods=['GET'])
@require_app_auth
def get_product(product_id):
    product = Product.objects(id=product_id).first()

    if not product:
        raise ApiException('product not found', 404)

    return render_json(me_to_json(product))

@products.route('/products', methods=['POST'])
@require_app_auth
def create_product():
    data = parse_request(request)

    new_product = Product(**{ k: v for (k, v) in data.iteritems() if k in Product._fields.keys() })
    new_product.save()

    return render_json(me_to_json(new_product), status=201)

@products.route('/products/<product_id>', methods=['PUT'])
@require_app_auth
def update_product(product_id):
    data = parse_request(request)

    known_fields = Product._fields.keys()

    # Mongoengine update doesn't support validation now
    # https://github.com/MongoEngine/mongoengine/issues/453
    # So, we use save()
    product = Product.objects(id=product_id).first()
    if not product:
        raise ApiException('product not found')

    for k, v in data.iteritems():
        if k in known_fields:
            setattr(product, k, v)
    product.save()

    return render_json(me_to_json(product))

@products.route('/products/<product_id>', methods=['DELETE'])
@require_app_auth
def delete_product(product_id):
    product = Product.objects(id=product_id).first()
    if not product:
        raise ApiException('product not found')
    product.delete()

    return render_json(me_to_json(product))
