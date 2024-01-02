from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    password1 = forms.CharField(max_length=30, required=True)
    password2 = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "password")
