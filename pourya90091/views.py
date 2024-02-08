from django.shortcuts import render
from django.contrib import messages


def index(req):
    notification = list(msg)[0] if (msg := messages.get_messages(req)) else None

    return render(req, "index.html", {
            "notification": notification
    })
