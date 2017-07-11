# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from main.forms import EmailForm
from main.mail_utils import MailSender


@require_POST
@csrf_exempt
def email_request(request):
    form = EmailForm(request.POST)

    mail_success = False
    status_code = 400
    if form.is_valid():
        sender = MailSender()
        mail_success = sender.send_mail_request(form.cleaned_data)
        if mail_success:
            status_code = 200

    return JsonResponse({"success": mail_success}, status=status_code)

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
                form = EmailForm()
    else:
        form = EmailForm()

    context = {
        'form': form,
        'mail_sent_to': mail_sent_to,
        'response_code': response_code
    }
    return render(request, 'main/email_form.html', context)
