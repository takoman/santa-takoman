# -*- coding: utf-8 -*-
from flask import Blueprint, request, send_from_directory

site = Blueprint('site', __name__, static_folder='static')

@site.route('/robots.txt', methods=['GET'])
def static_from_root():
    return send_from_directory(site.static_folder, request.path[1:])
