
from django import forms

class EmailForm(forms.Form):

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