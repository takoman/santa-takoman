# -*- coding: utf-8 -*-

from flask import current_app as app
import os, mandrill

class MandrillAPI(object):
    def __init__(self):
        self.api_key = os.environ.get('MANDRILL_API_KEY') or app.config.get('MANDRILL_API_KEY')

    def send_email(self,
                   to_name=None,
                   to_email=None,
                   from_name=None,
                   from_email=None,
                   subject=None,
                   cc=None,
                   bcc=None,
                   reply_to=None,
                   html=None,
                   sent_at=None,
                   opens_count=0,
                   clicks_count=0,
                   postman_send_id=None,
                   track_clicks=True,
                   track_opens=True,
                   test=False,
                   tags=[],
                   ga_campaign=None):

        self.message = {
            'attachments': [],
            'auto_html': None,
            'auto_text': None,
            'bcc_address': bcc,
            'from_email': from_email,
            'from_name': from_name,
            'google_analytics_campaign': ga_campaign,
            'google_analytics_domains': ['takoman.co'],
            'headers': {'Reply-To': from_email},
            'html': html,
            'images': [],
            'important': False,
            'inline_css': None,
            'merge': True,
            'merge_vars': [],
            'metadata': {'website': 'takoman.co'},
            'preserve_recipients': None,
            'recipient_metadata': [],
            'return_path_domain': None,
            'signing_domain': None,
            'subaccount': None,
            'subject': subject,
            'tags': tags,
            'text': '',
            'to': [{'email': to_email, 'name': to_name, 'type': 'to'}],
            'track_clicks': track_clicks,
            'track_opens': track_opens,
            'tracking_domain': None,
            'url_strip_qs': None,
            'view_content_link': None
        }

        try:
            m = mandrill.Mandrill(self.api_key)
            result = m.messages.send(message=self.message, async=True)

        except mandrill.Error, e:
            # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'    
            raise StandardError(
                'A mandrill error occurred: %s - %s' % (e.__class__, e))
