from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views import View
from django.http import HttpRequest, Http404
from article.forms import ArticleForm
from article.models import Article
import markdown


User = get_user_model()


class ArticleView(View):
    def get(self, req: HttpRequest, username, slug):
        user = User.objects.filter(username__exact=username).first()
        article_exists = Article.objects.filter(slug__iexact=slug, user__exact=user).exists()
        if article_exists:
            article = Article.objects.filter(slug__iexact=slug, user__exact=user).first()
            md = markdown.Markdown(extensions=["fenced_code"])
            article.content = md.convert(article.content)
            return render(req, "article/article.html", {
                "article": article
            })

        raise Http404()


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
