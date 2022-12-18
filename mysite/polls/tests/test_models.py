from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ..models import Question


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
