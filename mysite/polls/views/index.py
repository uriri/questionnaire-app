from django.utils import timezone
from django.views import generic

from ..models import Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_questions"

    def get_queryset(self):
        return Question.objects.filter(publish_at__lte=timezone.now()).order_by(
            "-publish_at"
        )[:5]
