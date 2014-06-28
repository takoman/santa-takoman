# -*- coding: utf-8 -*-

from flask import Blueprint, request
from santa.models.domain.client_app import ClientApp
from santa.lib.common import parse_request, render_json, me_to_json
from santa.lib.auth import require_app_auth
import json, datetime

client_apps = Blueprint('client_apps', __name__)

@client_apps.route('/api/v1/client_apps', methods=['GET'])
def get_client_apps():
    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')
    client_app = ClientApp.objects(client_id=client_id, client_secret=client_secret).first()

    data = {}
    if client_app:
        # Ideally, we have to expire tokens periodically and generate new ones.
        # Here we just expire it in 10 years.
        ten_years_from_now = datetime.datetime.now() + datetime.timedelta(days=10 * 365)
        expires = ten_years_from_now.isoformat()
        data = { u'xapp_token': client_app['token'], u'expires_in': expires }

    return render_json(json.dumps(data))

@client_apps.route('/api/v1/client_apps/<client_app_id>', methods=['GET'])
@require_app_auth
def get_client_app(client_app_id):
    client_app = ClientApp.objects(id=client_app_id).first()

    return render_json(me_to_json(client_app))
