from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    activate_code = models.CharField(max_length=64, blank=False, default=None)
