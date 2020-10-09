from http import HTTPStatus

from django.test import TestCase
from django.urls import resolve, reverse
from mock import patch

from apps.feedback.views import FeedbackUsabilityView
from apps.feedback.forms import FeedbackUsabilityForm, FeelingTypes
from tests.feedback.constants import ErrorHTML


class TestFeedbackUsabilityViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("feedback:usability")

    def test_summary_url_resolves_to_correct_view(self):
        match = resolve("/feedback/usability/")
        assert match.func.view_class == FeedbackUsabilityView

    def test_feedback_splash_view_loads_correct_template(self):
        response = self.client.get(self.url)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, "feedback/usability.html")

    @patch.object(FeedbackUsabilityForm, 'save')
    def test_submitting_invalid_form(self, mock_save):
        response = self.client.post(self.url, {})
        html = response.content.decode('utf8')
        form = response.context['form']

        assert HTTPStatus.OK == response.status_code
        assert form.is_valid() is False
        self.assertFormError(response, 'form', 'feeling_type', "This field is required.")
        assert ErrorHTML.FIELD_ERROR in html
        assert mock_save.called is False

    @patch.object(FeedbackUsabilityForm, 'save')
    def test_submitting_valid_form_calls_to_forms_api(self, mock_form_save):
        redirect_url = reverse("feedback:thank-you")
        data = {"feeling_type": FeelingTypes.VERY_SATISFIED}
        response = self.client.post(self.url, data)

        assert mock_form_save.called
        self.assertRedirects(response, redirect_url)
