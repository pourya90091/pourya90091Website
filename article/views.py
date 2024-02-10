from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views import View
from django.http import HttpRequest
from article.forms import ArticleForm
from article.models import Article


class ArticleView(View):
    def get(self, req: HttpRequest, slug):
        pass

    def post(self, req: HttpRequest, slug):
        pass


@method_decorator(login_required, name='dispatch')
class CreateArticleView(View):
    def get(self, req: HttpRequest):
        return render(req, "article/create_article.html", {
            "article_form": ArticleForm()
        })

    def post(self, req: HttpRequest):
        article_form = ArticleForm(req.POST)
        if article_form.is_valid():
            title = article_form.cleaned_data.get("title")
            content = article_form.cleaned_data.get("content")

            new_article = Article(title=title,
                                  user=req.user,
                                  content=content)
            new_article.save()

            return redirect(reverse("dashboard"))

        return render(req, "article/create_article.html", {
            "article_form": article_form
        })
