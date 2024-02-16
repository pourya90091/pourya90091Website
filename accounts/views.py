from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.urls import reverse
# from accounts.models import User
from django.views import View
from django.http import HttpRequest, Http404
from accounts.forms import SignUpForm, LoginForm, LogoutForm, RecoverPasswordForm, ChangePasswordForm
from utils.authorize import redirect_logged_in_user
from utils.email import send_email
from dotenv import load_dotenv
import os
import re


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

            user_exists = User.objects.filter(username__exact=username).exists()
            if user_exists:
                signup_form.add_error("username", "Username is already taken.")
                data_is_valid = False

            user_exists = User.objects.filter(email__iexact=email).exists()
            if user_exists:
                signup_form.add_error("email", "Email is already taken.")
                data_is_valid = False

            if password != confirm_password:
                signup_form.add_error("password", "Password not confirmed correctly.")
                data_is_valid = False

            return data_is_valid

        signup_form = SignUpForm(req.POST, req.FILES)
        if signup_form.is_valid():
            username = signup_form.cleaned_data.get("username")
            password = signup_form.cleaned_data.get("password")
            confirm_password = signup_form.cleaned_data.get("confirm_password")
            email = signup_form.cleaned_data.get("email")
            profile_image = signup_form.files.get("profile_image")

            data_is_valid = data_validation()
            if data_is_valid:
                new_user = User(username=username,
                                email=email,
                                is_active=True,
                                is_email_active=False,
                                activate_code=get_random_string(64),
                                profile_image=profile_image)
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

            user = User.objects.filter(username__exact=username).first()

            data_is_valid = data_validation()
            if data_is_valid:
                login(req, user)
                url = req.build_absolute_uri()
                return redirect(
                    reverse("dashboard")
                    if "?next" not in url
                    else re.search(r"\?next=(.+)$", url)[1]
                )

        return render(req, "accounts/login.html", {
            "login_form": login_form
        })


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, req: HttpRequest):
        return render(req, "accounts/logout.html", {
            "logout_form": LogoutForm()
        })

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


@method_decorator(login_required, name='dispatch')
class EmailVerificationView(View):
    def get(self, req: HttpRequest):
        if req.user.email:
            url = f"{BASE_URL}{reverse('activate_account', args=[req.user.activate_code])}"
            send_email("Email Verification", req.user.email, {"url": url}, "email/email_verification.html")
            msg = "Check your mailbox."
        else:
            msg = "You have not any email to verify."

        messages.add_message(req, messages.SUCCESS, msg)
        return redirect(reverse("dashboard"))


@method_decorator(login_required, name='dispatch')
class ActivateView(View):
    def get(self, req: HttpRequest, activate_code):
        if activate_code != req.user.activate_code:
            raise Http404()

        if not req.user.is_email_active:
            req.user.is_email_active = True
            req.user.activate_code = get_random_string(64)
            req.user.save()

            msg = "Your email has been verified."
        else:
            msg = "Your email has already been verified."

        messages.add_message(req, messages.SUCCESS, msg)
        return redirect(reverse("dashboard"))


class RecoverPasswordView(View):
    def get(self, req: HttpRequest):
        return render(req, "accounts/recover_password.html", {
            "recover_password_form": RecoverPasswordForm()
        })

    def post(self, req: HttpRequest):
        def data_validation():
            data_is_valid = True

            user_exists = User.objects.filter(email__iexact=email).exists()
            if not user_exists:
                recover_password_form.add_error("email", "There is no user with that email.")
                data_is_valid = False

            return data_is_valid

        recover_password_form = RecoverPasswordForm(req.POST)
        if recover_password_form.is_valid():
            email = recover_password_form.cleaned_data.get("email")

            data_is_valid = data_validation()
            if data_is_valid:
                user = User.objects.filter(email__iexact=email).first()
                url = f"{BASE_URL}{reverse('change_password', args=[user.activate_code])}"
                send_email("Recover Password", email, {"url": url}, "email/recover_password.html")
                messages.add_message(req, messages.SUCCESS, "Check your mailbox.")

                return redirect(reverse("index"))

        return render(req, "accounts/recover_password.html", {
            "recover_password_form": recover_password_form
        })


class ChangePasswordView(View):
    def check_activate_code(func):
        def wrapper(*args, **kwargs):
            activate_code = kwargs["activate_code"]
            user_exists = User.objects.filter(activate_code__exact=activate_code).exists()
            if not user_exists:
                raise Http404()
            return func(*args, **kwargs)
        return wrapper

    @check_activate_code
    def get(self, req: HttpRequest, activate_code):
        return render(req, "accounts/change_password.html", {
            "change_password_form": ChangePasswordForm()
        })

    @check_activate_code
    def post(self, req: HttpRequest, activate_code):
        def data_validation():
            data_is_valid = True

            if new_password != confirm_new_password:
                change_password_form.add_error("new_password", "New password not confirmed correctly.")
                data_is_valid = False

            return data_is_valid

        change_password_form = ChangePasswordForm(req.POST)
        if change_password_form.is_valid():
            new_password = change_password_form.cleaned_data.get("new_password")
            confirm_new_password = change_password_form.cleaned_data.get("confirm_new_password")

            data_is_valid = data_validation()
            if data_is_valid:
                user = User.objects.filter(activate_code__exact=activate_code).first()
                user.set_password(new_password)
                user.activate_code = get_random_string(64)
                user.save()

                return redirect(reverse("index"))

        return render(req, "accounts/change_password.html", {
            "change_password_form": change_password_form
        })
