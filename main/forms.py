
from django import forms
from django.conf import settings

from bs4 import BeautifulSoup

class HtmlTextField(forms.CharField):

    def to_python(self, value):
        if not value:
            return None
        return BeautifulSoup(value, 'html.parser').get_text()


class EmailForm(forms.Form):

    # The form that creates and validates email submissions. The top 3 methods clean the form fields in specific ways,
    # usually parsing out HTML.

    CLIENT_CHOICES = [
        (settings.MAIL_MAILGUN, 'Mailgun'),
        (settings.MAIL_SENDGRID, 'Sendgrid'),
    ]

    def clean_subject(self):
        # Subject is required even once all the HTML is parsed out.
        sbj = self.cleaned_data['subject']
        if sbj:
            sbj = BeautifulSoup(sbj, 'html.parser').get_text()
            if len(sbj) == 0:
                raise forms.ValidationError("Subject must be valid once HTML is parsed out.")
        return sbj

    def clean_body(self):
        # Body is required even once all the HTML is parsed out.
        body = self.cleaned_data['body']
        if body:
            body = BeautifulSoup(body, 'html.parser').get_text()
            if len(body) == 0:
                raise forms.ValidationError("Body must be valid once HTML is parsed out.")
        return body

    def clean_mail_client(self):
        if self.cleaned_data.get('mail_client'):
            return int(self.cleaned_data['mail_client'])
        return None

    mail_client = forms.ChoiceField(
        label="Email Service Provider",
        choices=CLIENT_CHOICES,
        initial=settings.MAIL_ACTIVE,
        required=False
    )

    from_name = forms.CharField(
        label="From Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    from_email = forms.EmailField(
        label="From Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    to_name = forms.CharField(
        label="To Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    to_email = forms.EmailField(
        label="To Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    subject = forms.CharField(
        label="Subject",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    body = forms.CharField(
        label="Body",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )