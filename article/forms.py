from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=64, required=True)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}), required=True)

    def __init__(self, title=None, content=None, *args, **kwargs) -> None:
        self.base_fields["title"].initial = title
        self.base_fields["content"].initial = content

        super().__init__(*args, **kwargs)
