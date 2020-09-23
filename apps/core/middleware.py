import json

from django.utils.deprecation import MiddlewareMixin

from apps.core.views import CookieToggle


class CookiesMiddleware(MiddlewareMixin):

    def get_cookie_settings(self, request):
        """
        Parses user cookies in the request and adjust the settings accordingly.
        :return: DICT - cookie settings
        """
        cookie_preferences_set = False
        settings = {
            "google_analytics": CookieToggle.OFF
        }
        current_cookie_settings = request.COOKIES.get("cookie_settings") or '{}'
        current_cookie_settings = json.loads(current_cookie_settings)
        if current_cookie_settings:
            cookie_preferences_set = True
        for option in settings.keys():
            if option in current_cookie_settings.keys():
                settings[option] = current_cookie_settings[option]

        return cookie_preferences_set, settings

    def process_request(self, request):
        """
        Load user's cookie preferences if any.
        """
        request.cookie_preferences_set, request.cookie_settings = self.get_cookie_settings(request)

    def process_response(self, request, response):
        return response
