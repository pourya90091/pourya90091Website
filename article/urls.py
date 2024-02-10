from django.urls import path
from article import views

urlpatterns = [
    path("<str:username>/<slug:slug>/", views.ArticleView.as_view(), name="article"),
    path("create/", views.CreateArticleView.as_view(), name="create_article"),
]
