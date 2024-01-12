from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest
from django.views import View
from panel.forms import ProfileForm
from utils.authorize import check_user_logged_in


User = get_user_model()


class PanelView(View):
    @check_user_logged_in
    def get(self, req: HttpRequest):
        notification = list(msg)[0] if (msg := messages.get_messages(req)) else None

        return render(req, "panel/dashboard.html", {
            "notification": notification,
            "user": req.user
        })


class ProfileView(View):
    @check_user_logged_in
    def get(self, req: HttpRequest):
        ProfileForm.set_placeholder(req.user.username, req.user.email)

        return render(req, "panel/profile.html", {
            "profile_form": ProfileForm()
        })

    @check_user_logged_in
    def post(self, req: HttpRequest):
        def data_validation():
            data_is_valid = True

            if username:
                user_exists = User.objects.filter(username__iexact=username).exists()
                if user_exists:
                    profile_form.add_error("username", "Username is already taken.")

            if not req.user.check_password(old_password):
                profile_form.add_error("old_password", "Old password is not correct.")
                data_is_valid = False

            if new_password != confirm_new_password:
                profile_form.add_error("confirm_new_password", "New password not confirmed correctly.")
                data_is_valid = False

            return data_is_valid

        profile_form = ProfileForm(req.POST)
        if profile_form.is_valid():
            username = profile_form.cleaned_data.get("username")
            old_password = profile_form.cleaned_data.get("old_password")
            new_password = profile_form.cleaned_data.get("new_password")
            confirm_new_password = profile_form.cleaned_data.get("confirm_new_password")
            email = profile_form.cleaned_data.get("email")

            data_is_valid = data_validation()
            if data_is_valid:
                req.user.username = username or req.user.username
                req.user.email = email or req.user.email
                req.user.set_password(new_password) if new_password else None
                req.user.save()

                return redirect(reverse("dashboard"))

        return render(req, "panel/profile.html", {
            "profile_form": profile_form
        })
