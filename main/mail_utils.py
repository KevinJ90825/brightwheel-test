import json

import requests
from django.conf import settings
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth


class MailSender(object):

    SENDGRID_API_ENDPOINT = "https://api.sendgrid.com/v3/mail/send"
    MAILGUN_API_ENDPOINT = "https://api.mailgun.net/v3/prbounty.co/messages"

    def send_mail_request(self, msg_data, mail_service=None):
        if not mail_service:
            mail_service = settings.MAIL_ACTIVE

        msg_data['subject'] = BeautifulSoup(msg_data['subject'], 'html.parser').get_text()
        msg_data['body'] = BeautifulSoup(msg_data['body'], 'html.parser').get_text()

        if mail_service == settings.MAIL_MAILGUN:
            return self.send_mailgun_request(msg_data)
        else:
            return self.send_sendgrid_request(msg_data)
        return 0


    def send_mailgun_request(self, msg_data):
        auth = HTTPBasicAuth("api:{}".format(settings.MAILGUN_API_KEY), "")
        formatted_data = {
            'from': '{} <{}>'.format(msg_data['from_name'], msg_data['from_email']),
            'to': '{} <{}>'.format(msg_data['to_name'], msg_data['to_email']),
            'subject': msg_data['subject'],
            'text': msg_data['body']
        }

        response = requests.post(
            self.MAILGUN_API_ENDPOINT, auth=auth, data=formatted_data)

        return response.status_code


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

