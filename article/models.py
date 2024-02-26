from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model


User = get_user_model()


class Article(models.Model):
    title = models.CharField(max_length=64, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    slug = models.SlugField(null=False, db_index=True)
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False)
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now)


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False)
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
