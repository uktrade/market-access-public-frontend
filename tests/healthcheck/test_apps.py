from django.apps import apps
from django.test import TestCase

from apps.healthcheck.apps import HealthcheckConfig


class HealthCheckConfigTestCase(TestCase):
    def test_apps(self):
        self.assertEqual(HealthcheckConfig.name, "apps.healthcheck")
        self.assertEqual(apps.get_app_config("healthcheck").name, "apps.healthcheck")
