from django.utils import timezone
from django.views import generic

from ..models import Question


class DetailView(generic.DetailView):
    """質問詳細ページ"""

    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """非公開のquestionを除外する"""
        return Question.objects.filter(publish_at__lte=timezone.now())
