from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """未来の日付は最近扱いに含まないテスト"""
        time = timezone.now() + timedelta(days=30)
        future_question = Question(publish_at=time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        """1日以上前の日付は最近扱いに含まないテスト"""
        time = timezone.now() - timedelta(days=1, seconds=1)
        old_question = Question(publish_at=time)
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        """24時間以内は最近扱いに含むテスト"""
        time = timezone.now() - timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(publish_at=time)
        self.assertTrue(recent_question.was_published_recently())


def create_question(question_text, days):
    time = timezone.now() + timedelta(days=days)
    return Question.objects.create(text=question_text, publish_at=time)


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
