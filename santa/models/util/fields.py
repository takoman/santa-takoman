# -*- coding: utf-8 -*-

from mongoengine import *
import bcrypt

class PasswordField(StringField):
    """
        PasswordField
            A simplified version of https://github.com/MongoEngine/extras-mongoengine/issues/8
    """
    def __init__(self, min_length=6, max_length=None, salt=None, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        self.salt = salt or bcrypt.gensalt()
        super(PasswordField, self).__init__(kwargs, min_length=min_length, max_length=max_length)

    def set_password(self, password):
        """
            Sets the user's password
                Example: $2a$12$OqyMEkjn19pe0.nIKnwnG.t1vHiMBBSlrtUdzuVGnjP9Ic7uS6ysm
        """
        encrypted_password = bcrypt.hashpw(password, self.salt)
        return encrypted_password

    def to_mongo(self, value):
        return self.set_password(value)

    def to_python(self, value):
        """
            Returns password
        """
        return value
