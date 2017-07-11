
from django import forms
from django.conf import settings

class EmailForm(forms.Form):

    CLIENT_CHOICES = [
        (settings.MAIL_MAILGUN, 'Mailgun'),
        (settings.MAIL_SENDGRID, 'Sendgrid'),
    ]

    mail_client = forms.ChoiceField(
        label="Email Service Provider",
        choices=CLIENT_CHOICES,
        initial=settings.MAIL_ACTIVE
    )

    from_name = forms.CharField(
        label="From Name",
        initial="KJ",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    from_email = forms.EmailField(
        label="From Email",
        initial="kevin@prbounty.co",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    to_name = forms.CharField(
        label="To Name",
        initial="Kevin Johnson",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    to_email = forms.EmailField(
        label="To Email",
        initial="kevin.w.johnson825@gmail.com",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    subject = forms.CharField(
        label="Subject",
        initial="Test Subject!",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    body = forms.CharField(
        label="Body",
        initial="<h1>Hello!</h1><p>How are you?</p>",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )