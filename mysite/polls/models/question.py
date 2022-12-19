from datetime import timedelta

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    text = models.CharField(max_length=200)
    publish_at = models.DateTimeField("date published")

    def __str__(self) -> str:
        return self.text

    @admin.display(
        boolean=True, ordering="publish_at", description="Published recently?"
    )
    def was_published_recently(self) -> bool:
        now = timezone.now()
        return now - timedelta(days=1) <= self.publish_at <= now
