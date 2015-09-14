# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from mongoengine.connection import get_connection

app = Blueprint('v1.system', __name__)

@app.route('/system/up', methods=['GET'])
def get_system_status():
    status = {
        'flask': True,
        'database': get_connection().alive()
    }
    return jsonify(**status)
