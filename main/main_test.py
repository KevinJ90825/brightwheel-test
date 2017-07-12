# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import requests
import datetime
import requests_mock

from django.urls import reverse

DEFAULT_PAYMENT = 200

def test_api_endpoint(settings, client):
    test_cases = [
        # The normal use case.
        (200, {'to_name': 'Kevin Johnson', 'to_email': 'kevin.w.johnson825@gmail.com', 'from_name': 'Test User',
               'from_email': 'test@example.com', 'subject': 'Hello!', 'body': 'This is a test!'}),
        # Normal use case with HTML in the body to parse out.
        (200, {'to_name': 'Kevin Johnson', 'to_email': 'kevin.w.johnson825@gmail.com', 'from_name': 'Test User',
               'from_email': 'test@example.com', 'subject': 'Hello!', 'body': '<h3>This is a test!</h3>'}),
    ]

    with requests_mock.Mocker() as mock:
        # Mock the email provider endpoints so requests aren't actually sent.
        mock.post(settings.MAILGUN_API_ENDPOINT, status_code=200, text=str(settings.MAIL_MAILGUN))
        mock.post(settings.SENDGRID_API_ENDPOINT, status_code=200, text=str(settings.MAIL_SENDGRID))

        for service, service_url in [
            (settings.MAIL_MAILGUN, settings.MAILGUN_API_ENDPOINT),
            (settings.MAIL_SENDGRID, settings.SENDGRID_API_ENDPOINT)]:
            for expected_response, test_data in test_cases:
                test_data['mail_client'] = service
                r = client.post(reverse('email'), data=test_data)

                assert r.status_code == expected_response
                if expected_response == 200:
                    assert int(r.json()['message']) == service
                    assert mock.last_request.netloc in service_url

def test_api_validation(settings, client):
    test_cases = [
        # Invalid request because the body is empty once the HTML is parsed out.
        (400, {'to_name': 'Kevin Johnson', 'to_email': 'kevin.w.johnson825@gmail.com', 'from_name': 'Test User',
               'from_email': 'test@example.com', 'subject': 'Hello!', 'body': '<h3></h3>'}),
        # Invalid request because to_email isn't a valid email format.
        (400, {'to_name': 'Kevin Johnson', 'to_email': 'Kevin Johnson', 'from_name': 'Test User',
               'from_email': 'test@example.com', 'subject': 'Hello!', 'body': 'This is a test!'}),
    ]

    with requests_mock.Mocker() as mock:
        # Mock the email provider endpoints so requests aren't actually sent.
        mock.post(settings.MAILGUN_API_ENDPOINT, status_code=200, text=str(settings.MAIL_MAILGUN))
        mock.post(settings.SENDGRID_API_ENDPOINT, status_code=200, text=str(settings.MAIL_SENDGRID))

        for service, service_url in [
            (settings.MAIL_MAILGUN, settings.MAILGUN_API_ENDPOINT),
            (settings.MAIL_SENDGRID, settings.SENDGRID_API_ENDPOINT)]:
            for expected_response, test_data in test_cases:
                test_data['mail_client'] = service
                r = client.post(reverse('email'), data=test_data)

                assert r.status_code == expected_response
                if expected_response == 200:
                    assert int(r.json()['message']) == service
                    assert mock.last_request.netloc in service_url
