from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=64, required=True, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Title"
    }))
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Markdown content..."
    }))

    def __init__(self, title=None, content=None, *args, **kwargs) -> None:
        self.base_fields["title"].initial = title
        self.base_fields["content"].initial = content

        super().__init__(*args, **kwargs)
