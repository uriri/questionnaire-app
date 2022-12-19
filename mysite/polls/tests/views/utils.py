from datetime import timedelta

from django.utils import timezone

from ...models import Question


def create_question(question_text, days):
    time = timezone.now() + timedelta(days=days)
    return Question.objects.create(text=question_text, publish_at=time)
