# -*- coding: utf-8 -*-

from jinja2 import Environment, PackageLoader

class EmailComposer(object):
    def __init__(self, template):
        self.template = template

class WelcomeEmailComposer(EmailComposer):
    def __init__(self, template):
        super(WelcomeEmailComposer, self).__init__(template)

    def compose_email(self):
        env = Environment(
            loader=PackageLoader('santa', 'apps/email/templates'))
        template = env.get_template(self.template)
        return template.render(year='2014')

    def get_email_params(self):
        return {
            'subject': '歡迎使用 Takoman 代購超人',
            'tags': ['welcome_eamil'],
            'ga_campaign': 'welcome'
        }

if __name__ == '__main__':
    composer = WelcomeEmailComposer('welcome.html')
    print composer.compose_email()
