from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True,
                               widget=forms.TextInput({'class': 'form-control',
                                                       'placeholder': 'username'}))
    email = forms.CharField(max_length=50, required=True,
                            widget=forms.EmailInput({'class': 'form-control',
                                                     'placeholder': 'username@gmail.com'}))
    first_name = forms.CharField(max_length=50, required=True,
                                 widget=forms.TextInput({'class': 'form-control',
                                                         'placeholder': 'first_name'}))
    last_name = forms.CharField(max_length=50, required=False,
                                widget=forms.TextInput({'class': 'form-control',
                                                        'placeholder': 'last_name'}))
    password1 = forms.CharField(max_length=50, min_length=5, required=True,
                                widget=forms.PasswordInput({'class': 'form-control',
                                                            'placeholder': 'password1'}))
    password2 = forms.CharField(max_length=50, min_length=5, required=True,
                                widget=forms.PasswordInput({'class': 'form-control',
                                                            'placeholder': 'password2'}))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, required=True,
                               widget=forms.TextInput({'class': 'form-control',
                                                       'placeholder': 'username'}))
    password = forms.CharField(max_length=50, min_length=5, required=True,
                               widget=forms.PasswordInput({'class': 'form-control',
                                                           'placeholder': 'password'}))

    class Meta:
        model = User
        fields = ["username", "password"]
