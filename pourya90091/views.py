from django.shortcuts import render
from django.urls import reverse


def index(req):
    return render(req, "index.html", {
        "login_url": reverse("login"),
        "signup_url": reverse("signup")
        })
