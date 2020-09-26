import json

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from apps.core.utils import get_future_date
from apps.core.views import CookieToggle


class CookiesMiddleware(MiddlewareMixin):

    def get_cookie_settings(self, request):
        """
        Parses user cookies in the request and adjust the settings accordingly.
        :return: DICT - cookie settings
        """
        cookie_settings = {
            settings.GOOGLE_ANALYTICS_COOKIE_NAME: CookieToggle.OFF
        }
        current_cookie_settings = request.COOKIES.get(settings.COOKIE_SETTINGS_COOKIE_NAME) or '{}'
        current_cookie_settings = json.loads(current_cookie_settings)

        for option in cookie_settings.keys():
            if option in current_cookie_settings.keys():
                cookie_settings[option] = current_cookie_settings[option]

        return cookie_settings

    def get_cookie_preferences_set(self, request):
        """
        Although there are other more sufficient ways to tell whether a user has set their cookie choices.
        To keep things consistent with gov.uk a cookie is used to track this.
        The presence of this cookie indicates that the user have set their cookie preference
        therefore they won't be prompted to tun their cookie preferences again.
        """
        return bool(request.COOKIES.get(settings.COOKIE_PREFERENCES_SET_COOKIE_NAME))

    def get_global_bar_seen(self, request):
        """
        There's a separate banner shown when users accept all cookies.
        The presence of this cookie indicates that the user have accepted all cookies
        and they have seen the confirmation banner.
        """
        seen = request.COOKIES.get(settings.GLOBAL_BAR_SEEN_COOKIE_NAME)
        if seen is not None:
            # False means the user was presented the banner
            # True means the user has either clicked the Hide button
            # or they navigated away from- or reloaded the page
            return json.loads(seen)
        else:
            return seen

    def process_request(self, request):
        """
        Load user's cookie preferences if any.
        """
        request.cookie_settings = self.get_cookie_settings(request)
        request.cookie_preferences_set = self.get_cookie_preferences_set(request)
        request.global_bar_seen = self.get_global_bar_seen(request) is not None

    def process_response(self, request, response):
        global_bar_seen = self.get_global_bar_seen(request)
        if global_bar_seen in (None, False):
            if request.cookie_preferences_set:
                value = False
                if global_bar_seen is False:
                    value = True
                response.set_cookie(
                    settings.GLOBAL_BAR_SEEN_COOKIE_NAME,
                    json.dumps(value),
                    expires=get_future_date(days=settings.COOKIE_SETTINGS_CONFIRMATION_BANNER)
                )

        return response
