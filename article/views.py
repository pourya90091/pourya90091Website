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
from article.models import Article, Comment, Reply
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

            comments = {}
            for comment in (comment for comment in Comment.objects.filter(article__exact=article).all()):
                comments[comment] = Reply.objects.filter(comment__exact=comment).all()

            return render(req, "article/article.html", {
                "article": article,
                "comments": comments,
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

            if "<script" in content: # decline attempt for using script tag
                article_form.add_error("content", "Seems like you want to use a script tag! Sorry but you can't.")
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

            if "<script" in content: # decline attempt for using script tag
                article_form.add_error("content", "Seems like you want to use a script tag! Sorry but you can't.")
                data_is_valid = False

            return data_is_valid

        article_form = ArticleForm(data=req.POST)
        if article_form.is_valid():
            title = article_form.cleaned_data.get("title")
            content = article_form.cleaned_data.get("content")

            data_is_valid = data_validation()
            if data_is_valid:
                article = Article.objects.filter(slug__iexact=slug, user__exact=req.user).first()

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
            nonlocal comment_id

            comment = Comment(user=user,
                            article=article,
                            content=comment)
            comment.save()

            comment_id = comment.id

        comment = req.POST['comment']
        article_id = req.POST['article_id']

        data_is_valid = data_validation()
        if data_is_valid:
            article = Article.objects.filter(pk__iexact=article_id).first()

            comment_id = None
            save_comment(req.user, article, comment)

            return Response({"comment": comment, "comment_id": comment_id, "username": req.user.username}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Data was not valid."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@method_decorator(login_required, name='dispatch')
class DeleteCommentAPIView(APIView):
    def post(self, req: HttpRequest):
        def data_validation():
            data_is_valid = True

            comment_exists = Comment.objects.filter(pk__iexact=comment_id, user__exact=req.user).exists()
            if not comment_exists:
                data_is_valid = False

            return data_is_valid

        comment_id = req.POST['comment_id']

        data_is_valid = data_validation()
        if data_is_valid:
            comment = Comment.objects.filter(pk__iexact=comment_id).first()
            comment.delete()

            return Response({"status": "OK"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Data was not valid."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@method_decorator(login_required, name='dispatch')
class ReplyAPIView(APIView):
    def post(self, req: HttpRequest):
        def data_validation():
            data_is_valid = True

            if not reply:
                data_is_valid = False

            comment_exists = Comment.objects.filter(pk__iexact=comment_id).exists()
            if not comment_exists:
                data_is_valid = False

            return data_is_valid

        def save_reply(user, comment, reply):
            nonlocal reply_id

            reply = Reply(user=user,
                          comment=comment,
                          content=reply)
            reply.save()

            reply_id = reply.id

        reply = req.POST['reply']
        comment_id = req.POST['comment_id']

        data_is_valid = data_validation()
        if data_is_valid:
            comment = Comment.objects.filter(pk__iexact=comment_id).first()

            reply_id = None
            save_reply(req.user, comment, reply)

            return Response({"reply": reply, "reply_id": reply_id, "username": req.user.username}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Data was not valid."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@method_decorator(login_required, name='dispatch')
class DeleteReplyAPIView(APIView):
    def post(self, req: HttpRequest):
        def data_validation():
            data_is_valid = True

            reply_exists = Reply.objects.filter(pk__iexact=reply_id, user__exact=req.user).exists()
            if not reply_exists:
                data_is_valid = False

            return data_is_valid

        reply_id = req.POST['reply_id']

        data_is_valid = data_validation()
        if data_is_valid:
            reply = Reply.objects.filter(pk__iexact=reply_id).first()
            reply.delete()

            return Response({"status": "OK"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Data was not valid."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
