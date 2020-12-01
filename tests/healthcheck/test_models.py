from django.test import TestCase

from apps.healthcheck.models import HealthCheck


class HealthCheckTestCase(TestCase):

    def test_default_values(self):
        item = HealthCheck.objects.create()
        assert True is item.health_check_field
        assert "True" == str(item)
        assert "<HealthCheck - True>" == repr(item)
