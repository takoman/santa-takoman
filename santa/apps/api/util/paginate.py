# -*- coding: utf-8 -*-

from santa.lib.api_errors import ApiException
from santa.apps.api.util.pagination import Pagination

def paginate(qs, params = {}):
    """ Paginate a query set.
    """
    page = params.get('page', 1, type=int)
    size = params.get('size', 10, type=int)
    if size > 100:
        raise ApiException('size param exceeds maximum 100')

    return Pagination(qs, page, size).items
