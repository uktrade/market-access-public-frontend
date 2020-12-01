import json

from distutils import util

from django import forms
from django.conf import settings
from django.urls import reverse_lazy

from django.views.generic import FormView, TemplateView

from apps.core.mixins import BreadcrumbsMixin
from apps.core.utils import get_future_date


class CookieToggle:
    OFF = False
    ON = True

    @classmethod
    def choices(cls):
        return (
            (cls.OFF, {"label": "OFF"}),
            (cls.ON, {"label": "ON"}),
        )


class CookieSettingsForm(forms.Form):
    # see - GOOGLE_ANALYTICS_COOKIE_NAME
    usage = forms.ChoiceField(choices=CookieToggle.choices,)


class CookiePolicyView(BreadcrumbsMixin, TemplateView):
    template_name = "pages/cookie-policy.html"
    breadcrumbs = (("Cookie Policy", reverse_lazy("core:cookie-policy")),)


class CookiesView(BreadcrumbsMixin, FormView):
    template_name = "pages/cookies.html"
    form_class = CookieSettingsForm
    breadcrumbs = (("Cookies", reverse_lazy("core:cookies")),)

    def get_success_url(self):
        return self.request.next or "/"

    def get_initial(self):
        data = super().get_initial()
        cookies = (settings.GOOGLE_ANALYTICS_COOKIE_NAME,)
        for item in cookies:
            # always opt in
            data[item] = self.request.cookie_settings.get(item) or CookieToggle.OFF
        return data

    def form_valid(self, form):
        response = super().form_valid(form)
        data = {}
        # convert from values to bool
        for k, v in form.cleaned_data.items():
            data[k] = bool(util.strtobool(v))
        settings_expires = get_future_date(days=settings.COOKIE_SETTINGS_EXPIRY)
        response.set_cookie(
            settings.COOKIE_SETTINGS_COOKIE_NAME,
            json.dumps(data),
            expires=settings_expires,
        )
        response.set_cookie(
            settings.COOKIE_PREFERENCES_SET_COOKIE_NAME,
            json.dumps(True),
            expires=settings_expires,
        )
        return response
