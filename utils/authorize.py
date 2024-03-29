from django.http import Http404, HttpRequest
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def check_user_logged_in(func):
    def wrapper(*args, **kwargs):
        req: HttpRequest = args[1]
        if req.user.username == "":
            raise Http404()
        return func(*args, **kwargs)
    return wrapper


def redirect_logged_in_user(func):
    def wrapper(*args, **kwargs):
        req: HttpRequest = args[1]
        if req.user.username:
            messages.add_message(req, messages.SUCCESS, "You are already logged in.")

            return redirect(reverse("dashboard"))
        return func(*args, **kwargs)
    return wrapper
