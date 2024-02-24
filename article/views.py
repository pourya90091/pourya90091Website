from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from django.http import HttpRequest, Http404
from article.forms import ArticleForm
from article.models import Article, Comment
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
                "article": article,
                "comments": Comment.objects.filter(article__exact=article).all(),
                "user": req.user
            })

        raise Http404()


class ArticlesView(View):
    def get(self, req: HttpRequest, username):
        user = User.objects.filter(username__exact=username).first()
        if not user:
            raise Http404()

        articles = Article.objects.filter(user__exact=user).all()
        if articles:
            return render(req, "article/articles.html", {
                "articles": articles,
                "user": user
            })

        return render(req, "article/articles.html", {
            "err": f"{user.username} have not published any articles yet."
        })


@method_decorator(login_required, name='dispatch')
class CreateArticleView(View):
    def get(self, req: HttpRequest):
        return render(req, "article/create_article.html", {
            "article_form": ArticleForm()
        })

    def post(self, req: HttpRequest):
        def data_validation():
            data_is_valid = True

            article_exists = Article.objects.filter(title__iexact=title, user__exact=req.user).exists()
            if article_exists:
                article_form.add_error("title", "You already have an article with this name.")
                data_is_valid = False

            return data_is_valid

        article_form = ArticleForm(data=req.POST)
        if article_form.is_valid():
            title = article_form.cleaned_data.get("title")
            content = article_form.cleaned_data.get("content")

            data_is_valid = data_validation()
            if data_is_valid:
                new_article = Article(title=title,
                                      user=req.user,
                                      content=content)
                new_article.save()

                return redirect(reverse("article", kwargs={'username': req.user.username, "slug": slugify(title)}))

        return render(req, "article/create_article.html", {
            "article_form": article_form
        })


@method_decorator(login_required, name='dispatch')
class EditArticleView(View):
    def get(self, req: HttpRequest, slug):
        article_exists = Article.objects.filter(slug__iexact=slug, user__exact=req.user).exists()
        if not article_exists:
            raise Http404()

        article = Article.objects.filter(slug__iexact=slug, user__exact=req.user).first()

        return render(req, "article/edit_article.html", {
            "article_form": ArticleForm(article.title, article.content)
        })

    def post(self, req: HttpRequest, slug):
        def data_validation():
            data_is_valid = True

            if slugify(title) != slug:
                article_exists = Article.objects.filter(title__iexact=title, user__exact=req.user).exists()
                if article_exists:
                    article_form.add_error("title", "You have another article with this name.")
                    data_is_valid = False

            return data_is_valid

        article_form = ArticleForm(data=req.POST)
        if article_form.is_valid():
            title = article_form.cleaned_data.get("title")
            content = article_form.cleaned_data.get("content")

            data_is_valid = data_validation()
            if data_is_valid:
                article = Article.objects.filter(slug__iexact=slugify(title), user__exact=req.user).first()

                article.title = title
                article.content = content
                article.save()

                return redirect(reverse("article", kwargs={'username': req.user.username, "slug": slugify(title)}))

        return render(req, "article/edit_article.html", {
            "article_form": article_form
        })


@method_decorator(login_required, name='dispatch')
class CommentAPIView(APIView):
    def post(self, req: HttpRequest):
        def data_validation():
            data_is_valid = True

            if not comment:
                data_is_valid = False

            article_exists = Article.objects.filter(pk__iexact=article_id).exists()
            if not article_exists:
                data_is_valid = False

            return data_is_valid

        def save_comment(user, article, comment):
            comment = Comment(user=user,
                            article=article,
                            content=comment)
            comment.save()

        comment = req.POST['comment']
        article_id = req.POST['article_id']

        data_is_valid = data_validation()
        if data_is_valid:
            article = Article.objects.filter(pk__iexact=article_id).first()

            save_comment(req.user, article, comment)

            return Response({"comment": comment, "username": req.user.username}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Data was not valid."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
