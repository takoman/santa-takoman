# -*- coding: utf-8 -*-

from datetime import datetime

DATE_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

def str_to_date(string):
    """ Converts a RFC-1123 string to the corresponding datetime value.

    :param string: the RFC-1123 string to convert to datetime value.
    """
    return datetime.strptime(string, DATE_FORMAT) if string else None


def date_to_str(date):
    """ Converts a datetime value to the corresponding RFC-1123 string.

    :param date: the datetime value to convert.
    """
    return datetime.strftime(date, DATE_FORMAT) if date else None
