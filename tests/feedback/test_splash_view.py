from http import HTTPStatus

from django.test import TestCase
from django.urls import resolve, reverse

from apps.feedback.forms import FeedbackTypes
from apps.feedback.views import FeedbackSplashView
from tests.feedback.constants import ErrorHTML


class TestFeedbackSplashViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("feedback:splash")

    def test_summary_url_resolves_to_correct_view(self):
        match = resolve("/feedback/")
        assert match.func.view_class == FeedbackSplashView

    def test_feedback_splash_view_loads_correct_template(self):
        response = self.client.get(self.url)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, "feedback/splash.html")

    def test_selecting_usability_redirects_to_correct_url(self):
        redirect_url = reverse("feedback:usability")
        data = {
            "feedback_type": FeedbackTypes.USABILITY,
        }

        response = self.client.post(self.url, data)

        self.assertRedirects(response, redirect_url)

    def test_selecting_issue_redirects_to_correct_url(self):
        redirect_url = reverse("feedback:issue")
        data = {
            "feedback_type": FeedbackTypes.ISSUE,
        }

        response = self.client.post(self.url, data)

        self.assertRedirects(response, redirect_url)

    def test_selecting_report_a_barrier_redirects_to_correct_url(self):
        redirect_url = reverse("feedback:barrier")
        data = {
            "feedback_type": FeedbackTypes.BARRIER,
        }

        response = self.client.post(self.url, data)

        self.assertRedirects(response, redirect_url)

    def test_submitting_empty_form_raises_an_error(self):
        response = self.client.post(self.url, {})
        html = response.content.decode("utf8")
        form = response.context["form"]

        assert HTTPStatus.OK == response.status_code
        assert form.is_valid() is False
        self.assertFormError(
            response, "form", "feedback_type", "This field is required."
        )
        assert ErrorHTML.FIELD_ERROR in html
