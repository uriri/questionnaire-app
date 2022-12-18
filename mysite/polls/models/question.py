from datetime import timedelta

from django.db import models
from django.utils import timezone


class Question(models.Model):
    text = models.CharField(max_length=200)
    publish_at = models.DateTimeField("date published")

    def __str__(self) -> str:
        return self.text

    def was_published_recently(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.publish_at <= now
