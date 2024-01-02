from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=80, required=True)
    confirm_password = forms.CharField(max_length=80, required=True)
    email = forms.EmailField(max_length=100)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=80, required=True)
