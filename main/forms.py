
from django import forms

class EmailForm(forms.Form):

    from_name = forms.CharField(
        label="From Name",
        initial="KJ",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    from_email = forms.EmailField(
        label="From Email",
        initial="kevin@homeward.io",
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