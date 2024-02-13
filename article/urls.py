from django.urls import path
from article import views

urlpatterns = [
    path("edit/<slug:slug>/", views.EditArticleView.as_view(), name="edit_article"),
    path("<str:username>/articles/", views.ArticlesView.as_view(), name="articles"),
    path("<str:username>/<slug:slug>/", views.ArticleView.as_view(), name="article"),
    path("create/", views.CreateArticleView.as_view(), name="create_article"),
]
