# -*- coding: utf-8 -*-

from santa.lib.api_errors import ApiException
from santa.apps.api.util.pagination import Pagination
from werkzeug.exceptions import NotFound

# TODO paginate helper should not coupled with MongoEnine and should accept
# pymongo cursor as its first argument instead.
def paginate(qs, params={}):
    """ Paginate a MongoEngine query set, and convert the results to a list
    of MongoEngine Documents.
    """
    try:
        page = int(params.get('page', 1))
        size = int(params.get('size', 10))
        if size > 100:
            raise ApiException('size param exceeds maximum 100')

        paginated = Pagination(qs, page, size).items
    except NotFound:
        paginated = []

    return paginated
