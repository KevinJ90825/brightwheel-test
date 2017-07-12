# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from main.forms import EmailForm
from main.mail_utils import MailSender


@require_POST
@csrf_exempt
def email_request(request):
    form = EmailForm(request.POST)

    status_code = 400
    response_data = {"success": False}
    if form.is_valid():
        sender = MailSender()
        mail_response = sender.send_mail_request(
            form.cleaned_data,
            mail_service=form.cleaned_data.get('mail_client')
        )
        if mail_response.ok:
            response_data["success"] = True
            status_code = 200

        response_data["message"] = mail_response.content

    return JsonResponse(response_data, status=status_code)

def index(request):
    response_code = -1
    mail_sent_to = None
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            sender = MailSender()
            mail_response = sender.send_mail_request(
                form.cleaned_data, mail_service=form.cleaned_data['mail_client'])
            if mail_response.ok:
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
