from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User, Interest
from django.core.exceptions import ValidationError


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

def validate_password(value, email, username):
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    if not any(char in r'!@#$%^&*()+[]{}|;:,.<>?/`~' for char in value):
        raise ValidationError("Password must contain at least one special character.")

    if not any(char.isdigit() for char in value):
        raise ValidationError("Password must contain at least one number.")

    if not any(char.isupper() for char in value):
        raise ValidationError("Password must contain at least one uppercase letter.")

    if not any(char.islower() for char in value):
        raise ValidationError("Password must contain at least one lowercase letter.")

    email_prefix = email.split('@')[0]
    if email_prefix in value:
        raise ValidationError("Password cannot contain the part of your email.")

    if username in value:
        raise ValidationError("Password cannot contain a substring of your username.")

class UserRegistrationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'email'}
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'username'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password'}
        )
    )
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        validate_password(password, email, username)

        return cleaned_data


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
        fields = ('full_name', 'email', 'interests')

    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')

        if not self.instance.check_password(current_password):
            raise forms.ValidationError("Invalid current password")

        return current_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            if len(new_password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")

            if not any(char in r'!@#$%^&*()+[]{}|;:,.<>?/`~' for char in new_password):
                raise forms.ValidationError("Password must contain at least one special character.")

            if not any(char.isdigit() for char in new_password):
                raise forms.ValidationError("Password must contain at least one number.")

            if not any(char.isupper() for char in new_password):
                raise forms.ValidationError("Password must contain at least one uppercase letter.")

            if not any(char.islower() for char in new_password):
                raise forms.ValidationError("Password must contain at least one lowercase letter.")
        return new_password

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
