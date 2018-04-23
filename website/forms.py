from django import forms
from django.utils.html import mark_safe


class ContactForm(forms.Form):

    first_name = forms.CharField(
        max_length=255, required=True,
        initial='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        max_length=255, required=True,
        initial='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
    )

    email_address = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
    )
    subject = forms.CharField(
        max_length=255, required=False,
        label='Subject',
        initial='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
    )

    cc = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
                'class': "regular-checkbox",
                'id': 'cc_id'
            }),
        label="Send me a copy of my email request",
        initial=True,
        required=False
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control email-message',
                                     'rows': 10}),
        label='Message',
        required=True)

    data_privacy_accepted = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': "regular-checkbox",
            'id': 'data_privacy_accepted_id'
        }),
        label=mark_safe(
            "I confirm I have reviewed and accept the terms of the "
            "<a href='/privacy-policy'>data privacy policy</a>"
        ),
        initial=False,
        required=False
    )

    def clean_data_privacy_accepted(self):
        # We hide the checkbox in order to style it, so we need to validate
        # on the backend instead of relying on the browser to do it
        accepted = self.cleaned_data.get('data_privacy_accepted', False)
        if not accepted:
            self.add_error(
                'data_privacy_accepted',
                'Please confirm you accept the terms of the data privacy '
                'agreement before submitting your request'
            )
        else:
            return accepted