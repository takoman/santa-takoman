# -*- coding: utf-8 -*-

from flask import Blueprint, request
from santa.lib.api_errors import ApiException
from santa.models.domain import *
from santa.lib.common import parse_request, render_json, me_to_json
from santa.lib.auth import require_app_auth
from santa.apps.api.util.paginate import paginate
from santa.apps.api.util.sort import sort
from mongoengine import *

app = Blueprint('v1.merchants', __name__)

@app.route('/merchants', methods=['GET'])
@require_app_auth
def get_merchants():
    merchants = Merchant.objects
    user_id = request.args.get('user_id', None)
    if user_id:
        merchants = merchants(user=user_id)

    paginated_and_sorted = paginate(sort(
        merchants, request.args), request.args)

    return render_json(me_to_json(paginated_and_sorted))

@app.route('/merchants/<merchant_id>', methods=['GET'])
@require_app_auth
def get_merchant(merchant_id):
    merchant = Merchant.objects(id=merchant_id).first()

    if not merchant:
        raise ApiException('merchant not found', 404)

    return render_json(me_to_json(merchant))

@app.route('/merchants', methods=['POST'])
@require_app_auth
def create_merchant():
    data = parse_request(request)

    new_merchant = Merchant(**{ k: v for (k, v) in data.iteritems() if k in Merchant._fields.keys() })
    new_merchant.save()

    return render_json(me_to_json(new_merchant), status=201)

@app.route('/merchants/<merchant_id>', methods=['PUT'])
@require_app_auth
def update_merchant(merchant_id):
    data = parse_request(request)

    known_fields = Merchant._fields.keys()
    merchant = Merchant.objects(id=merchant_id).first()
    if not merchant:
        raise ApiException('merchant not found', 404)

    for k, v in data.iteritems():
        if k in known_fields:
            # TODO: Unable to assign and save() a ReferenceField with a string ObjectId.
            # It will raise a ValidationError. We have to assign it with the actual document.
            # If there is no better way to do this, we have to refactor this into a helper.
            # http://stackoverflow.com/questions/28139533/mongoengine-document-unable-to-save-a-referencefield-with-a-string-objectid
            if (isinstance(Merchant._fields[k], ReferenceField)):
                v = Merchant._fields[k].document_type.objects(id=v).first()
                if not v:
                    raise ApiException(k + ' not found')
            setattr(merchant, k, v)
    merchant.save()

    return render_json(me_to_json(merchant))

@app.route('/merchants/<merchant_id>', methods=['DELETE'])
@require_app_auth
def delete_merchant(merchant_id):
    merchant = Merchant.objects(id=merchant_id).first()

    if not merchant:
        raise ApiException('merchant not found', 404)

    merchant.delete()

    return render_json(me_to_json(merchant))
