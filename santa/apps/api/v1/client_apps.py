# -*- coding: utf-8 -*-

from flask import Blueprint, request
from santa.models.domain.client_app import ClientApp
from santa.lib.common import render_json
import json, datetime

app = Blueprint('v1.client_apps', __name__)

@app.route('/xapp_token', methods=['GET'])
def get_client_apps():
    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')
    client_app = ClientApp.objects(client_id=client_id, client_secret=client_secret).first()

    data = {}
    if client_app:
        # Ideally, we have to expire tokens periodically and generate new ones.
        # Here we just expire it in 10 years.
        ten_years_from_now = datetime.datetime.utcnow() + datetime.timedelta(days=10 * 365)
        expires = ten_years_from_now.isoformat()
        data = { u'xapp_token': client_app['token'], u'expires_in': expires }

    return render_json(json.dumps(data))
