from django import forms
from django.core.validators import URLValidator


class PageUrlForm(forms.Form):
    page_url = forms.URLField(
        label='Enter an article URL',
        max_length=1500,
        validators=
        [URLValidator(message='Please enter a valid URL')]
    )


class PageTextForm(forms.Form):
    page_text = forms.CharField(widget=forms.Textarea(attrs={
        "rows": 20,
        "cols": 20,
        "class": "materialize-textarea",
        "style": "height: 100px",
    }), label='Copy and paste the text you would like to learn into this input field:')
