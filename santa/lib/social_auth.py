# -*- coding: utf-8 -*-

import facebook

class SocialFacebook:
    def get_auth_data(self, oauth_token):
        try:
            graph = facebook.GraphAPI(oauth_token)
            profile = graph.get_object("me")
            auth_data = {
                'uid': profile.get('id'),
                'name': profile.get('name'),
                'email': profile.get('email'),
                'info': profile,
                'provider': 'facebook'
            }
        except facebook.GraphAPIError:
            auth_data = None

        return auth_data
