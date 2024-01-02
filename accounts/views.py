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
        return render(req, "accounts/signup.html", {
            "signup_form": SignUpForm()
        })

    def post(self, req: HttpRequest):
        signup_form = SignUpForm(req.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data.get("username")
            password = signup_form.cleaned_data.get("password")
            confirm_password = signup_form.cleaned_data.get("confirm_password")
            email = signup_form.cleaned_data.get("email")

            user_exists = User.objects.filter(username__iexact=username).exists()
            if user_exists:
                signup_form.add_error("username", "Username is already taken.")

            if not password == confirm_password:
                signup_form.add_error("password", "Password not confirmed correctly.")
            else:
                new_user = User(username=username,
                                email=email)
                new_user.set_password(password)
                new_user.save()

                return redirect(reverse("index"))

        return render(req, "accounts/signup.html", {
            "signup_form": signup_form
        })


class LoginView(View):
    def get(self, req: HttpRequest):
        return render(req, "accounts/login.html", {
            "login_form": LoginForm()
        })

    def post(self, req: HttpRequest):
        login_form = LoginForm(req.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")

            user = User.objects.filter(username__iexact=username).first()
            if user:
                if user.check_password(password):
                    login(req, user)
                    return redirect(reverse("index"))
                else:
                    login_form.add_error("password", "Password is not correct")
            else:
                login_form.add_error("username", "There is no user with that username.")

        return render(req, "accounts/login.html", {
            "login_form": login_form
        })
