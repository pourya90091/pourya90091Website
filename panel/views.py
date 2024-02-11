from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.http import HttpRequest
from django.views import View
from panel.forms import ProfileForm


User = get_user_model()


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, req: HttpRequest):
        notification = list(msg)[0] if (msg := messages.get_messages(req)) else None

        return render(req, "panel/dashboard.html", {
            "notification": notification,
            "user": req.user
        })


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, req: HttpRequest):
        ProfileForm.set_placeholder(req.user.username, req.user.email)

        return render(req, "panel/profile.html", {
            "profile_form": ProfileForm()
        })

    def post(self, req: HttpRequest):
        def data_validation():
            data_is_valid = True

            if username:
                user_exists = User.objects.filter(username__exact=username).exists()
                if user_exists:
                    profile_form.add_error("username", "Username is already taken.")
                    data_is_valid = False

            if not req.user.check_password(current_password):
                profile_form.add_error("current_password", "Current password is not correct.")
                data_is_valid = False

            if new_password != confirm_new_password:
                profile_form.add_error("confirm_new_password", "New password not confirmed correctly.")
                data_is_valid = False

            return data_is_valid

        profile_form = ProfileForm(req.POST)
        if profile_form.is_valid():
            username = profile_form.cleaned_data.get("username")
            email = profile_form.cleaned_data.get("email")
            current_password = profile_form.cleaned_data.get("current_password")
            new_password = profile_form.cleaned_data.get("new_password")
            confirm_new_password = profile_form.cleaned_data.get("confirm_new_password")

            data_is_valid = data_validation()
            if data_is_valid:
                if username:
                    req.user.username = username
                if email:
                    # if the new email was not same as old email, then is_email_active should be False
                    req.user.is_email_active = email == req.user.email
                    req.user.email = email
                if new_password:
                    req.user.set_password(new_password)

                req.user.save()

                return redirect(reverse("dashboard"))

        return render(req, "panel/profile.html", {
            "profile_form": profile_form
        })
