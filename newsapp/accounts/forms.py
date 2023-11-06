from django import forms
from django.contrib.auth.forms import UserChangeForm

from . import models

from .models import User, Interest


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'email'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password'}
        )
    )


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'email'}
        )
    )
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'full name'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password'}
        )
    )


class ManagerLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'email'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password'}
        )
    )


class EditProfileForm(UserChangeForm):
    new_password = forms.CharField(
        label="New Password",
        required=False,  # New password is optional
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ('full_name', 'email', 'interests', 'is_manager')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # Remove the password fields from the form instance
        del self.fields['password']

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')

        if not self.instance.check_password(current_password):
            raise forms.ValidationError("Invalid current password")

        return current_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            return new_password
        return None


class InterestsForm(forms.ModelForm):
    user_email = forms.EmailField(label='Your Email')

    class Meta:
        model = Interest
        fields = ['name']

    name = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super(InterestsForm, self).__init__(*args, **kwargs)
        self.fields['name'].queryset = Interest.objects.all()
