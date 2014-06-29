# -*- coding: utf-8 -*-

from mongoengine import *
from mongoengine import signals
import datetime, bcrypt
from santa.lib.common import parse_request, render_json, me_to_json
from santa.models.domain.social_auth import SocialAuth
from santa.apps.email.models.emailer import Emailer
from santa.apps.email.models.composer import WelcomeEmailComposer
from santa.apps.email.models.mandrill_api import MandrillAPI

class User(Document):
    name        = StringField(max_length=200, required=True)
    email       = EmailField(max_length=200, required=True, unique=True)
    password    = StringField(max_length=200)
    slug        = StringField(max_length=200)
    role        = ListField(StringField(choices=[u'user', u'takoman', u'admin']))
    updated_at  = DateTimeField(default=datetime.datetime.now)
    created_at  = DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'users'
    }

    @classmethod
    def normalize_user(cls, sender, document, **kwargs):
        user = document
        if user.password:
            user.password = bcrypt.hashpw(user.password, bcrypt.gensalt())
        user.email = user.email.lower()

        return

    def link_social_auth(self, social_auth_data):
        data = {'uid': social_auth_data.get('uid'), 'user': self}
        if 'info' in social_auth_data:
            for field in ['name', 'email', 'nickname', 'first_name', 'last_name', 'location', 'description', 'image', 'phone']:
                data[field] = social_auth_data['info'].get(field)
            if social_auth_data['info'].get('urls'):
                data['urls'] = social_auth_data['info'].get('urls')

        if 'credentials' in social_auth_data:
            data['credentials'] = social_auth_data['credentials']

        # TODO flush any complex objects from extra hash
        if 'extra' in social_auth_data:
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

signals.pre_save.connect(User.normalize_user, sender=User)
