from http import HTTPStatus

from django.test import TestCase
from django.urls import resolve, reverse

from apps.feedback.views import FeedbackBarrierView


class TestFeedbackBarrierViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("feedback:barrier")

    def test_summary_url_resolves_to_correct_view(self):
        match = resolve("/feedback/barrier/")
        assert match.func.view_class == FeedbackBarrierView

    def test_feedback_splash_view_loads_correct_template(self):
        response = self.client.get(self.url)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, "feedback/barrier.html")
