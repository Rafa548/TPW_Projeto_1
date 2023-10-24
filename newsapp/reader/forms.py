# forms.py
from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search', 'class': 'form-control'}))
