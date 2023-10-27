# forms.py
from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search', 'class': 'form-control'}))

class NewsSaveForm(forms.Form):
    news_url = forms.URLField()
    news_title = forms.CharField(max_length=200)
    news_description = forms.CharField(max_length=300)
    news_image = forms.URLField()
    news_publishedat = forms.DateTimeField()