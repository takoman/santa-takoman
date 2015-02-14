# -*- coding: utf-8 -*-

from flask import Blueprint, request
from santa.lib.api_errors import ApiException
from santa.models.domain import *
from santa.lib.common import parse_request, render_json, me_to_json
from santa.lib.auth import require_app_auth
from santa.apps.api.util.paginate import paginate
from santa.apps.api.util.sort import sort
from mongoengine import *

payment_accounts = Blueprint('payment_accounts', __name__)

@payment_accounts.route('/payment_accounts', methods=['GET'])
@require_app_auth
def get_payment_accounts():
    paginated_and_sorted = paginate(sort(PaymentAccount.objects, request.args), request.args)

    return render_json(me_to_json(paginated_and_sorted))

@payment_accounts.route('/payment_accounts/<payment_account_id>', methods=['GET'])
@require_app_auth
def get_payment_account(payment_account_id):
    payment_account = PaymentAccount.objects(id=payment_account_id).first()

    if not payment_account:
        raise ApiException('payment account not found', 404)

    return render_json(me_to_json(payment_account))

@payment_accounts.route('/payment_accounts', methods=['POST'])
@require_app_auth
def create_payment_account():
    data = parse_request(request)

    new_payment_account = PaymentAccount(**{ k: v for (k, v) in data.iteritems() if k in PaymentAccount._fields.keys() })

    new_payment_account.save()

    return render_json(me_to_json(new_payment_account), status=201)

@payment_accounts.route('/payment_accounts/<payment_account_id>', methods=['PUT'])
@require_app_auth
def update_payment_account(payment_account_id):
    data = parse_request(request)

    known_fields = PaymentAccount._fields.keys()
    payment_account = PaymentAccount.objects(id=payment_account_id).first()
    if not payment_account:
        raise ApiException('payment account not found', 404)

    for k, v in data.iteritems():
        if k in known_fields:
            if (isinstance(PaymentAccount._fields[k], ReferenceField)):
                v = PaymentAccount._fields[k].document_type.objects(id=v).first()
                if not v:
                    raise ApiException(k + ' not found')
            setattr(payment_account, k, v)
    payment_account.save()

    return render_json(me_to_json(payment_account))

@payment_accounts.route('/payment_accounts/<payment_account_id>', methods=['DELETE'])
@require_app_auth
def delete_payment_account(payment_account_id):
    payment_account = PaymentAccount.objects(id=payment_account_id).first()

    if not payment_account:
        raise ApiException('payment account not found', 404)

    payment_account.delete()

    return render_json(me_to_json(payment_account))

