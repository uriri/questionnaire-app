from datetime import timedelta

from django.db import models
from django.utils import timezone


class Question(models.Model):
    text = models.CharField(max_length=200)
    publish_at = models.DateTimeField("date published")

    def __str__(self) -> str:
        return self.text

    def was_published_recently(self):
        return self.publish_at >= timezone.now() - timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.text
