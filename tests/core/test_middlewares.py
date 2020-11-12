from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings


class XRobotsMiddlewareTestCase(TestCase):

    def test_middleware_missing_setting(self):
        """
        Validate that the middleware raises configuration error
        if the setting is missing.
        """
        with self.assertRaisesMessage(
                ImproperlyConfigured,
                "X_ROBOTS_TAG is missing from django settings."
        ):
            self.client.get("/")

    @override_settings(X_ROBOTS_TAG=("wibble", "wobble"))
    def test_middleware_response_with_header(self):
        """
        Validate that the middleware sets X-Robots-Tag as per django settings
        """
        response = self.client.get("/")
        self.assertIn("x-robots-tag", response._headers)
        self.assertEqual(
            response._headers.get("x-robots-tag"),
            ("X-Robots-Tag", "wibble,wobble"),
        )

    @override_settings(X_ROBOTS_TAG=None)
    def test_middleware_response_without_header(self):
        """
        Validate that the middleware sets X-Robots-Tag as per django settings
        """
        response = self.client.get("/")
        self.assertNotIn("x-robots-tag", response._headers)
