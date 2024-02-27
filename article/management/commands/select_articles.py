from article.models import Article
from django.core.management.base import BaseCommand
from django.conf import settings
import schedule
import random
import time
import pickle


class Command(BaseCommand):
    help = "Select specific articles for showing in home page."
    
    def handle(self, *args, **options):
        schedule.every(1).hour.do(update_recent_articles)
        schedule.every(1).day.do(update_daily_articles)

        while True:
            schedule.run_pending()
            time.sleep(1)


def update_recent_articles():
    articles = Article.objects.all().order_by("-id")[:10]

    with open(f"{settings.BASE_DIR}/RECENT_ARTICLES.article", "wb") as file:
        pickle.dump(articles, file)


def update_daily_articles():
    articles_length = len(Article.objects.all())
    article_ids = random.sample(range(1, articles_length), 10)
    articles = []

    for article_id in article_ids:
        article = Article.objects.filter(pk__iexact=article_id).first()
        articles.append(article)

    with open(f"{settings.BASE_DIR}/DAILY_ARTICLES.article", "wb") as file:
        pickle.dump(articles, file)
