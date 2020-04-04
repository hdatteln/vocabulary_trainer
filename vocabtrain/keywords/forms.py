from django import forms

class PageUrlForm(forms.Form):
    page_url = forms.CharField(label='Enter an article URL', max_length=1500)
