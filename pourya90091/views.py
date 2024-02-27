from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
import pickle


def index(req):
    with open(f"{settings.BASE_DIR}/RECENT_ARTICLES.article", "rb") as file:
        RECENT_ARTICLES = pickle.load(file)

    with open(f"{settings.BASE_DIR}/DAILY_ARTICLES.article", "rb") as file:
        DAILY_ARTICLES = pickle.load(file)

    notification = list(msg)[0] if (msg := messages.get_messages(req)) else None

    return render(req, "index.html", {
            "daily_articles": DAILY_ARTICLES,
            "recent_articles": RECENT_ARTICLES,
            "notification": notification
    })
