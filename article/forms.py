from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=64, required=True)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}), required=True)
