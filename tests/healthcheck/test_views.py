import xml.etree.ElementTree as ET

from django.test import Client, TestCase

from apps.healthcheck.models import HealthCheck


class TestHealthcheckViews(TestCase):
    def setUp(self):
        self.anonymous_client = Client()

    def test_check_view(self):
        response = self.anonymous_client.get("/check/")
        tree = ET.fromstring(response.content)
        pingdom_status = tree[0].text
        pingdom_response_time = float(tree[1].text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(pingdom_status, "OK")
        self.assertGreater(pingdom_response_time, 0)
        self.assertLess(pingdom_response_time, 1)

    def test_check_view_no_data_fail(self):
        HealthCheck.objects.all().delete()
        response = self.anonymous_client.get("/check/")
        tree = ET.fromstring(response.content)
        pingdom_status = tree[0].text
        pingdom_response_time = float(tree[1].text)
        self.assertGreater(pingdom_response_time, 0)
        self.assertLess(pingdom_response_time, 1)
        self.assertEqual(pingdom_status, "FAIL")
        self.assertEqual(response.status_code, 200)
