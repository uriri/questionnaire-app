from django.test import TestCase
from django.urls import reverse

from .utils import create_question


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """未来日付のquestionは404を返す"""
        future_question = create_question("Future question.", 5)
        url = reverse("polls:detail", args=(future_question.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """過去日付、公開範囲内のquestionは表示する"""
        past_question = create_question("Past question.", -5)
        url = reverse("polls:detail", args=(past_question.id,))

        response = self.client.get(url)
        self.assertContains(response, past_question.text)
