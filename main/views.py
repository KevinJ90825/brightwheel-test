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
    mail_sent_to = None

    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            sender = MailSender()
            mail_success = sender.send_mail_request(
                form.cleaned_data, mail_service=int(form.cleaned_data['mail_client']))
            if mail_success:
                mail_sent_to = "{} ({})".format(form.cleaned_data['to_name'], form.cleaned_data['to_email'])

    context = {
        'form': EmailForm(),
        'mail_sent_to': mail_sent_to,
        'send_client': "Mailgun" if settings.MAIL_MAILGUN == settings.MAIL_ACTIVE else "Sendgrid",
        'response_code': response_code
    }
    return render(request, 'main/email_form.html', context)
