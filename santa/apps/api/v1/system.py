# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from mongoengine.connection import get_connection

system = Blueprint('system', __name__)

@system.route('/system/up', methods=['GET'])
def get_system_status():
    status = {
        'flask': True,
        'database': get_connection().alive()
    }
    return jsonify(**status)
