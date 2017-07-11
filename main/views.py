# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings


# Create your views here.
from django.views.decorators.http import require_POST

from main.forms import EmailForm
from main.mail_utils import MailSender


@require_POST
def email_request(request):
    sender = MailSender()
    sender.send_mail_request(request.POST)
    x=3

def index(request):
    response_code = -1
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            sender = MailSender()
            response_code = sender.send_mail_request(
                form.cleaned_data, mail_service=int(form.cleaned_data['mail_client']))

    context = {
        'form': EmailForm(),
        'send_client': "Mailgun" if settings.MAIL_MAILGUN == settings.MAIL_ACTIVE else "Sendgrid",
        'response_code': response_code
    }
    return render(request, 'main/email_form.html', context)
