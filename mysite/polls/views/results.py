from django.views import generic

from ..models import Question


class ResultsView(generic.DetailView):
    """質問結果ページ"""

    model = Question
    template_name = "polls/results.html"
