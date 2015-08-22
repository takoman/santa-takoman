# -*- coding: utf-8 -*-

from mongoengine import *
from santa.models.domain.social_auth import SocialAuth
from santa.apps.email.models.emailer import Emailer
from santa.apps.email.models.composer import WelcomeEmailComposer
from santa.apps.email.models.mandrill_api import MandrillAPI
from santa.models.mixins.updated_at_mixin import UpdatedAtMixin
from santa.models.util.fields import PasswordField
import datetime

__all__ = ('User',)

class User(UpdatedAtMixin, Document):
    name                  = StringField(max_length=200, required=True)
    email                 = EmailField(max_length=200, required=True, unique=True)
    password              = PasswordField(max_length=200)
    phone                 = StringField(max_length=50)
    slug                  = StringField(max_length=200)
    role                  = ListField(StringField(choices=[u'user', u'takoman', u'admin']), default=[u'user'])
    # Anonymous session
    anonymous             = BooleanField(default=False)
    anonymous_session_id  = StringField(max_length=200)
    updated_at            = DateTimeField(default=datetime.datetime.utcnow)
    created_at            = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'users'
    }

    def clean(self):
        """Pre validation/data cleaning"""
        if self.email:
            self.email = self.email.lower()

    def link_social_auth(self, social_auth_data):
        data = {'uid': social_auth_data.get('uid'), 'user': self}
        if 'info' in social_auth_data:
            for field in ['name', 'email', 'nickname', 'first_name', 'last_name', 'location', 'description', 'image', 'phone']:
                data[field] = social_auth_data['info'].get(field)
            if social_auth_data['info'].get('urls'):
                data['urls'] = social_auth_data['info'].get('urls')

        if social_auth_data.get('credentials'):
            data['credentials'] = social_auth_data['credentials']

        # TODO flush any complex objects from extra hash
        if social_auth_data.get('extra'):
            pass

        social_auth = SocialAuth(**data)
        social_auth.save()

        return

    def send_welcome_email(self):
        postman = MandrillAPI()
        composer = WelcomeEmailComposer('welcome.html')
        emailer = Emailer(to_name=self.name,
                          to_email=self.email,
                          postman=postman,
                          composer=composer)
        emailer.send_email()
