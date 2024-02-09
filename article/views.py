from django.shortcuts import render
from django.views import View
from django.http import HttpRequest


class ArticleView(View):
    def get(self, req: HttpRequest, slug):
        pass

    def post(self, req: HttpRequest, slug):
        pass
