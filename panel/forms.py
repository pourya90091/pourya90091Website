from django import forms


# getProfileForm is a wrapper to generate ProfileForm
def getProfileForm(username_placeholder, email_placeholder):
    class ProfileForm(forms.Form):
        username = forms.CharField(max_length=64, required=True, widget=forms.TextInput(attrs={
            "placeholder": username_placeholder
        }))
        old_password = forms.CharField(max_length=128, required=True)
        new_password = forms.CharField(max_length=128, required=True)
        confirm_new_password = forms.CharField(max_length=128, required=True)
        email = forms.EmailField(max_length=128, required=False, widget=forms.TextInput(attrs={
            "placeholder": email_placeholder
        }))

    return ProfileForm()
