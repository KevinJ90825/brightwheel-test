import json

import requests
from django.conf import settings
from bs4 import BeautifulSoup

class MailSender(object):

    SENDGRID_API_ENDPOINT = "https://api.sendgrid.com/v3/mail/send"

    def send_mail_request(self, msg_data):
        msg_data['subject'] = BeautifulSoup(msg_data['subject'], 'html.parser').get_text()
        msg_data['body'] = BeautifulSoup(msg_data['body'], 'html.parser').get_text()

        if settings.MAIL_ACTIVE == settings.MAIL_MAILGUN:
            self.send_mailgun_request(msg_data)
        else:
            return self.send_sendgrid_request(msg_data)
        return 0


    def send_mailgun_request(self, msg_data):
        pass


    def send_sendgrid_request(self, msg_data):
        headers = {
            'Authorization': 'Bearer {}'.format(settings.SENDGRID_API_KEY),
            'Content-Type': 'application/json'
        }

        formatted_data = {
            'personalizations': [
                {
                    'to': [{
                        'email': msg_data['to_email'],
                        'name': msg_data['to_name']
                    }],
                    'subject': msg_data['subject']
                }
            ],
            'from': {
                'email': msg_data['from_email'],
                'name': msg_data['from_name']
            },
            'content': [
                {
                    'type': 'text/plain',
                    'value': msg_data['body']
                }
            ]
        }

        response = requests.post(
            self.SENDGRID_API_ENDPOINT,
            headers=headers,
            data=json.dumps(formatted_data)
        )
        return response.status_code

