# -*- coding: utf-8 -*-

from mongoengine import *
from santa.lib.api_errors import ApiException

class UpdatableMixin(object):

    def update_with_dict(self, data):
        """Update the document with data passed in as a dict. Unknown
        fields will simply be ignored. A Referencefield can be an ObjectId,
        a string ObjectId, or a dict. If it is a dict, it will use the
        `_id` or `id` value of the dict.

        :param data: Data as a dict
        """
        def find_maybe_nested_ref_doc(k, v):
            klass = self.__class__
            ret = v
            if isinstance(klass._fields[k], ReferenceField):
                str_id = v
                if isinstance(v, dict):
                    str_id = v.get("_id") or v.get("id")
                if str_id is None:
                    raise ApiException(k + ' is not a valid dict of a ReferenceField (missing _id or id)')
                ret = klass._fields[k].document_type.objects(id=str_id).first()
                if ret is None:
                    raise ApiException(k + ' not found')
            return ret

        data = dict(data)  # make a copy

        if ("id" in data) and (data["id"] != str(self.id)):
            raise ApiException('unable to update %s with data with a different id' % self.__class__.__name__)

        data.pop("id", None)

        klass = self.__class__
        self.update(**{
            k: find_maybe_nested_ref_doc(k, v)
            for (k, v) in data.iteritems() if k in klass._fields.keys()
        })
