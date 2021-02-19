from django.apps import apps
from django.test import TestCase

from apps.metadata.apps import MetadataConfig


class MetadataConfigTestCase(TestCase):
    def test_apps(self):
        self.assertEqual(MetadataConfig.name, "apps.metadata")
        self.assertEqual(apps.get_app_config("metadata").name, "apps.metadata")
