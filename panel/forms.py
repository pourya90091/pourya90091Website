from django import forms


class ProfileForm(forms.Form):
    username = forms.CharField(max_length=64, required=False, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "New Username"
    }))
    email = forms.EmailField(max_length=128, required=False, widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "New Email"
    }))
    profile_image = forms.ImageField(allow_empty_file=False, required=False)
    current_password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Current Password"
    }))
    new_password = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "New Password"
    }))
    confirm_new_password = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm New Password"
    }))
