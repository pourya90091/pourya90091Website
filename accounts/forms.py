from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=64, required=True)
    password = forms.CharField(max_length=128, required=True)
    confirm_password = forms.CharField(max_length=128, required=True)
    email = forms.EmailField(max_length=128, required=False)
    profile_image = forms.ImageField(allow_empty_file=False, required=False)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, required=True)
    password = forms.CharField(max_length=128, required=True)


class LogoutForm(forms.Form):
    password = forms.CharField(max_length=128, required=True)


class RecoverPasswordForm(forms.Form):
    email = forms.EmailField(max_length=128, required=True)


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(max_length=128, required=True)
    confirm_new_password = forms.CharField(max_length=128, required=True)
