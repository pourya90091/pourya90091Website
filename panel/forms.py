from django import forms


class ProfileForm(forms.Form):
    username = forms.CharField(max_length=64, required=False)
    email = forms.EmailField(max_length=128, required=False)
    old_password = forms.CharField(max_length=128, required=True)
    new_password = forms.CharField(max_length=128, required=False)
    confirm_new_password = forms.CharField(max_length=128, required=False)

    @classmethod
    def set_placeholder(cls, username_placeholder, email_placeholder):
        cls.base_fields["username"].widget=forms.TextInput(attrs={
            "placeholder": username_placeholder
        })
        cls.base_fields["email"].widget=forms.TextInput(attrs={
            "placeholder": email_placeholder
        })
