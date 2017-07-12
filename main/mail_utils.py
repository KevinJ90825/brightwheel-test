import json

import requests
from django.conf import settings


class MailSender(object):

    def send_mail_request(self, msg_data, mail_service=None):
        # Param: msg_data must have keys: from_name, from_email, to_name, to_email, subject, and body.
        # Param: mail_service should be an integer representing settings.MAIL_MAILGUN or settings.MAIL_SENDGRID
        if not mail_service:
            mail_service = settings.MAIL_ACTIVE

        if mail_service == settings.MAIL_MAILGUN:
            return self.send_mailgun_request(msg_data)
        else:
            return self.send_sendgrid_request(msg_data)


    def send_mailgun_request(self, msg_data):
        formatted_data = {
            'from': '{} <{}>'.format(msg_data['from_name'], msg_data['from_email']),
            'to': '{} <{}>'.format(msg_data['to_name'], msg_data['to_email']),
            'subject': msg_data['subject'],
            'text': msg_data['body']
        }

        response = requests.post(
            settings.MAILGUN_API_ENDPOINT,
            auth=('api', settings.MAILGUN_API_KEY),
            data=formatted_data,
        )

        return response


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
            settings.SENDGRID_API_ENDPOINT,
            headers=headers,
            data=json.dumps(formatted_data)
        )
        return response

