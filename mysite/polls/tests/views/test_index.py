from django.test import TestCase
from django.urls import reverse

from .utils import create_question


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """questionが存在しない場合"""
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_questions"], [])

    def test_past_question(self):
        """表示される範囲下限値の過去question"""
        question = create_question("Past question", -30)

        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_questions"], [question])

    def test_future_question(self):
        """表示されない未来日付question"""
        _ = create_question("Future question", 30)

        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_questions"], [])

    def test_future_question_and_past_question(self):
        """表示されない未来日付questionと表示される範囲下限値の過去question"""
        question = create_question("Past question", -30)
        _ = create_question("Future question", 30)

        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_questions"], [question])

    def test_two_past_questions(self):
        """複数のquestionが表示される"""
        question1 = create_question("Past question 1.", -30)
        question2 = create_question("Past question 2.", -5)

        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_questions"], [question2, question1]
        )
