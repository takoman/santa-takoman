# -*- coding: utf-8 -*-

import arrow

def str_to_date(string):
    """ Converts a ISO-8601 string to the corresponding datetime value.

    :param string: the ISO-8601 string to convert to datetime value.
    """
    return arrow.get(string).to('utc').naive if string else None


def date_to_str(date):
    """ Converts a naive datetime value to the corresponding ISO-8601 string.

    :param date: the datetime value to convert.
    """
    return arrow.get(date).isoformat() if date else None
