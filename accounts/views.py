from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.urls import reverse
# from accounts.models import User
from django.views import View
from django.http import HttpRequest, Http404
from accounts.forms import SignUpForm, LoginForm, LogoutForm
from utils.authorize import check_user_logged_in, redirect_logged_in_user
from utils.email import send_email
from dotenv import load_dotenv
import os


load_dotenv()
BASE_URL = os.getenv("BASE_URL")

User = get_user_model()


class SignUpView(View):
    @redirect_logged_in_user
    def get(self, req: HttpRequest):
        return render(req, "accounts/signup.html", {
            "signup_form": SignUpForm()
        })

    @redirect_logged_in_user
    def post(self, req: HttpRequest):
        def data_validation():
            data_is_valid = True

            user_exists = User.objects.filter(username__iexact=username).exists()
            if user_exists:
                signup_form.add_error("username", "Username is already taken.")
                data_is_valid = False

            if password != confirm_password:
                signup_form.add_error("password", "Password not confirmed correctly.")
                data_is_valid = False

            return data_is_valid

        signup_form = SignUpForm(req.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data.get("username")
            password = signup_form.cleaned_data.get("password")
            confirm_password = signup_form.cleaned_data.get("confirm_password")
            email = signup_form.cleaned_data.get("email")

            data_is_valid = data_validation()
            if data_is_valid:
                new_user = User(username=username,
                                email=email,
                                is_active=False,
                                activate_code=get_random_string(64))
                new_user.set_password(password)
                new_user.save()

                login(req, new_user)
                return redirect(reverse("dashboard"))

        return render(req, "accounts/signup.html", {
            "signup_form": signup_form
        })


class LoginView(View):
    @redirect_logged_in_user
    def get(self, req: HttpRequest):
        return render(req, "accounts/login.html", {
            "login_form": LoginForm()
        })

    @redirect_logged_in_user
    def post(self, req: HttpRequest):
        def data_validation():
            data_is_valid = True

            if not user:
                login_form.add_error("username", "There is no user with that username.")
                data_is_valid = False
            else:
                if not user.check_password(password):
                    login_form.add_error("password", "Password is not correct")
                    data_is_valid = False

            return data_is_valid

        login_form = LoginForm(req.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")

            user = User.objects.filter(username__iexact=username).first()

            data_is_valid = data_validation()
            if data_is_valid:
                login(req, user)
                return redirect(reverse("dashboard"))

        return render(req, "accounts/login.html", {
            "login_form": login_form
        })


class LogoutView(View):
    @check_user_logged_in
    def get(self, req: HttpRequest):
        return render(req, "accounts/logout.html", {
            "logout_form": LogoutForm()
        })

    @check_user_logged_in
    def post(self, req: HttpRequest):
        def data_validation():
            data_is_valid = True

            if not req.user.check_password(password):
                logout_form.add_error("password", "Password is not correct")
                data_is_valid = False

            return data_is_valid

        logout_form = LogoutForm(req.POST)
        if logout_form.is_valid():
            password = logout_form.cleaned_data.get("password")

            data_is_valid = data_validation()
            if data_is_valid:
                logout(req)
                return redirect(reverse("index"))

        return render(req, "accounts/logout.html", {
            "logout_form": logout_form
        })


class ActivateView(View):
    @check_user_logged_in
    def get(self, req: HttpRequest, activate_code):
        if activate_code != req.user.activate_code:
            raise Http404()

        if not req.user.is_active:
            req.user.is_active = True
            req.user.activate_code = get_random_string(64)
            req.user.save()

            msg = "Your email has been verified."
        else:
            msg = "Your email has already been verified."

        messages.add_message(req, messages.SUCCESS, msg)
        return redirect(reverse("dashboard"))


class EmailVerificationView(View):
    @check_user_logged_in
    def get(self, req: HttpRequest):
        if req.user.email:
            url = f"{BASE_URL}{reverse('activate_account', args=[req.user.activate_code])}"  
            send_email("Email Verification", req.user.email, {"url": url}, "email/email_verification.html")
            msg = "Check your mailbox."
        else:
            msg = "You have not any email to verify."

        messages.add_message(req, messages.SUCCESS, msg)
        return redirect(reverse("dashboard"))
