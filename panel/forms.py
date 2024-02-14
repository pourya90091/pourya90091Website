from django import forms


class ProfileForm(forms.Form):
    username = forms.CharField(max_length=64, required=False)
    email = forms.EmailField(max_length=128, required=False)
    profile_image = forms.ImageField(allow_empty_file=False, required=False)
    current_password = forms.CharField(max_length=128, required=True)
    new_password = forms.CharField(max_length=128, required=False)
    confirm_new_password = forms.CharField(max_length=128, required=False)

    def __init__(self, username_placeholder=None, email_placeholder=None, *args, **kwargs) -> None:
        self.base_fields["username"].widget=forms.TextInput(attrs={
            "placeholder": username_placeholder
        } if username_placeholder else None)
        self.base_fields["email"].widget=forms.TextInput(attrs={
            "placeholder": email_placeholder
        } if email_placeholder else None)

        super().__init__(*args, **kwargs)
