from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.utils.crypto import get_random_string
from django.urls import reverse
# from accounts.models import User
from django.views import View
from django.http import Http404, HttpRequest
from accounts.forms import SignUpForm, LoginForm


User = get_user_model()


class SignUpView(View):
    def get(self, req: HttpRequest):
        pass

    def post(self, req: HttpRequest):
        pass


class LoginView(View):
    def get(self, req: HttpRequest):
        pass

    def post(self, req: HttpRequest):
        pass
