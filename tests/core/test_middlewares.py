from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings


class XRobotsMiddlewareTestCase(TestCase):
    @override_settings()
    def test_middleware_missing_setting(self):
        """
        Validate that the middleware raises configuration error
        if the setting is missing.
        """
        del settings.X_ROBOTS_TAG
        with self.assertRaisesMessage(
            ImproperlyConfigured, "X_ROBOTS_TAG is missing from django settings."
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


class ZipkinTracingMiddlewareTestCase(TestCase):
    """
    Validate that the middleware only sets X-B3-* headers if they are present in
    the request.
    """

    def test_middleware_response_without_headers(self):
        response = self.client.get("/")
        self.assertNotIn("x-b3-traceid", response._headers)
        self.assertNotIn("x-b3-spanid", response._headers)

    def test_middleware_response_with_headers(self):
        headers = {
            "HTTP_X-B3-TraceId": "wibble",
            "HTTP_X-B3-SpanId": "wobble",
        }
        response = self.client.get("/", **headers)

        self.assertIn("x-b3-traceid", response._headers)
        self.assertEqual(
            response._headers.get("x-b3-traceid"),
            ("X-B3-TraceId", "wibble"),
        )
        self.assertIn("x-b3-spanid", response._headers)
        self.assertEqual(
            response._headers.get("x-b3-spanid"),
            ("X-B3-SpanId", "wobble"),
        )

    def test_middleware_sets_zipkin_http_headers_on_request(self):
        headers = {
            "HTTP_X-B3-TraceId": "wibble",
            "HTTP_X-B3-SpanId": "wobble",
        }
        expected_headers = {
            "X-B3-TraceId": "wibble",
            "X-B3-SpanId": "wobble",
        }
        response = self.client.get("/", **headers)

        request = response.context_data["view"].request
        assert expected_headers == request.zipkin_http_headers

    def test_middleware_sets_zipkin_http_headers_on_request__empty(self):
        """
        Test that there are no zipkin headers set by default.
        """
        response = self.client.get("/")

        request = response.context_data["view"].request
        assert {} == request.zipkin_http_headers
