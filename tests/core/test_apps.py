from django.apps import apps
from django.test import TestCase

from apps.core.apps import CoreConfig


class CoreConfigTestCase(TestCase):
    def test_apps(self):
        self.assertEqual(CoreConfig.name, 'apps.core')
        self.assertEqual(apps.get_app_config("core").name, 'apps.core')
