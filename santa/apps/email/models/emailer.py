# -*- coding: utf-8 -*-

class Emailer(object):
    """Encapsulates and sends an email message.
    
    :param to_name: recipient name
    :param to_email: recipient email address
    :param from_name: sender name
    :param from_email: sender email address
    :param subject: email subject header
    :param cc: CC list
    :param bcc: BCC list
    :param reply_to: reply-to email address
    :param body: plain text message
    :param html: HTML message
    :param sent_at: send date
    :param opens_count: opens count
    :param clicks_count: clicks count
    :param postman_send_id: email service send ID
    :param track_clicks: if track clicks
    :param track_opens: if track opens
    :param test: if testing email
    :param postman: the email service, e.g. Mandrill
    :param composer: the email writer
    """

    def __init__(self,
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
                 postman_send_id=None,
                 postman=None,
                 composer=None):

        self.to_name = to_name
        self.to_email = to_email
        self.from_name = from_name or 'Takoman (代購超人)'
        self.from_email = from_email or 'it@takoman.co'
        self.subject = subject
        self.reply_to = reply_to or 'it@takoman.co'
        self.cc = cc
        self.bcc = bcc
        self.html = html
        self.sent_at = sent_at
        self.postman_send_id = postman_send_id
        self.postman = postman
        self.composer = composer

    def create_message(self):
        # Merge email params from composer with params from emailer.
        message = self.composer.get_email_params() or {}
        message.update((k, v) for k, v in {
            'to_name': self.to_name,
            'to_email': self.to_email,
            'from_name': self.from_name,
            'from_email': self.from_email,
            'subject': self.subject,
            'cc': self.cc,
            'bcc': self.bcc,
            'reply_to': self.reply_to,
            'html': self.composer.compose_email(),
            'track_clicks': True,
            'track_opens': True,
            'test': False
        }.iteritems() if v is not None)

        return message

    def send_email(self):
        if not all([self.postman, self.composer]):
            raise StandardError(
                "emailer needs to have a postman and a composer")

        message = self.create_message()

        if not all([message.get('to_email'), message.get('subject'), message.get('html')]):
            raise StandardError(
                "email should have receipient email, subject, and body")

        return self.postman.send_email(**message)

if __name__ == '__main__':
    from mandrill_api import MandrillAPI
    from composer import WelcomeEmailComposer
    import flask
    postman = MandrillAPI()
    composer = WelcomeEmailComposer('welcome.html')
    app = flask.Flask(__name__, template_folder='../templates')
    with app.app_context():
        email = Emailer(to_name='Pingchieh Chang',
                        to_email='pingchiehchang@gmail.com',
                        subject='歡迎使用 Takoman 代購超人',
                        postman=postman,
                        composer=composer)
        email.send_email()
