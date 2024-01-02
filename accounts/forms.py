from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=80, required=True)
    confirm_password = forms.CharField(max_length=80, required=True)
    email = forms.EmailField(max_length=100)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=80, required=True)
