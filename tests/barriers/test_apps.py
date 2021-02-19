from django.apps import apps
from django.test import TestCase

from apps.barriers.apps import BarriersConfig


class BarriersConfigTestCase(TestCase):
    def test_apps(self):
        self.assertEqual(BarriersConfig.name, "apps.barriers")
        self.assertEqual(apps.get_app_config("barriers").name, "apps.barriers")
