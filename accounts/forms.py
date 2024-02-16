from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=64, required=True, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))
    confirm_password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm Password"
    }))
    email = forms.EmailField(max_length=128, required=False, widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))
    profile_image = forms.ImageField(allow_empty_file=False, required=False)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, required=True, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))


class LogoutForm(forms.Form):
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))


class RecoverPasswordForm(forms.Form):
    email = forms.EmailField(max_length=128, required=True, widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "New Password"
    }))
    confirm_new_password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm New Password"
    }))
