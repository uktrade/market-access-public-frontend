from http import HTTPStatus

from django.test import TestCase
from django.urls import resolve, reverse

from apps.core.views import CookieToggle, CookiesView


class CookieToggleTestCase(TestCase):
    def test_choices(self):
        toggle = CookieToggle()
        toggle_label_choices = [v["label"] for k, v in toggle.choices()]
        assert 2 == len(toggle_label_choices)
        assert "ON" in toggle_label_choices
        assert "OFF" in toggle_label_choices


class CookiesViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("core:cookies")

    def test_cookies_url_resolves_to_correct_view(self):
        match = resolve("/cookies/")
        assert match.func.view_class == CookiesView

    def test_cookies_view_loads_correct_template(self):
        response = self.client.get(self.url)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, "pages/cookies.html")

    def test_cookies_set_usage_to_on(self):
        """ usage refers to google analytics """
        data = {"usage": True}

        response = self.client.post(self.url, data)

        assert HTTPStatus.FOUND == response.status_code
        assert '{"usage": true}' == response.cookies["cookies_policy"].value
        assert "true" == response.cookies["cookies_preferences_set"].value

    def test_cookies_set_usage_to_off(self):
        """ usage refers to google analytics """
        data = {"usage": False}

        response = self.client.post(self.url, data)

        assert HTTPStatus.FOUND == response.status_code
        assert '{"usage": false}' == response.cookies["cookies_policy"].value
        assert "true" == response.cookies["cookies_preferences_set"].value

    def test_cookies_set_usage__invalid_data(self):
        data = {"wibble": False}

        response = self.client.post(self.url, data)

        assert HTTPStatus.OK == response.status_code
        assert "cookies_policy" not in response.cookies.keys()
        assert "cookies_preferences_set" not in response.cookies.keys()

    def test_cookies_set_usage_to_on__default_redirect_url(self):
        """ Default redirect url is the index page / """
        data = {"usage": True}

        response = self.client.post(self.url, data)

        assert HTTPStatus.FOUND == response.status_code
        assert "/" == response.url

    def test_cookies_set_usage_to_on__with_next_in_query_params(self):
        """ Take redirect url from next= query param if present """
        data = {"usage": True}

        url = f"{self.url}?next=/wobble/"
        response = self.client.post(url, data)

        assert HTTPStatus.FOUND == response.status_code
        assert "/wobble/" == response.url
