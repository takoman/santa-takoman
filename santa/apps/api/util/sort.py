# -*- coding: utf-8 -*-

# TODO Considering raising unsupported sorting type if passed in invalid sort.
def sort(qs, params={}):
    """ Sort a MongoEngine query set. The order may be specified by prepending
    each of the keys by a + or a -. Ascending order is assumed. Multiple orders
    can be specified by concating each one with a ",".
    """
    sorted_qs = qs
    sort = params.get('sort', None)
    if sort:
        sorted_qs = qs.order_by(*sort.split(','))

    return sorted_qs
