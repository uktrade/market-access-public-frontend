from django.apps import apps
from django.test import TestCase

from apps.feedback.apps import FeedbackConfig


class FeedbackConfigTestCase(TestCase):
    def test_apps(self):
        self.assertEqual(FeedbackConfig.name, 'apps.feedback')
        self.assertEqual(apps.get_app_config("feedback").name, 'apps.feedback')
