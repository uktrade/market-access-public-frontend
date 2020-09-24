import datetime
import json

from django import forms
from django.conf import settings
from django.urls import reverse_lazy

from django.views.generic import FormView, TemplateView

from apps.core.mixins import BreadcrumbsMixin


class CookieToggle:
    OFF = 0
    ON = 1

    @classmethod
    def choices(cls):
        return (
            (
                cls.OFF,
                {
                    "label": "OFF"
                }
            ),
            (
                cls.ON,
                {
                    "label": "ON"
                }
            )
        )


class CookieSettingsForm(forms.Form):
    google_analytics = forms.ChoiceField(
        choices=CookieToggle.choices,
    )


class CookiePolicyView(BreadcrumbsMixin, TemplateView):
    template_name = "pages/cookie-policy.html"
    breadcrumbs = (
        ("Cookie Policy", reverse_lazy("core:cookie-policy")),
    )


class CookiesView(FormView):
    template_name = "pages/cookies.html"
    form_class = CookieSettingsForm
    breadcrumbs = (
        ("Cookies", reverse_lazy("core:cookies")),
    )

    def get_success_url(self):
        return self.request.next or "/"

    def get_initial(self):
        data = super().get_initial()
        cookies = ("google_analytics",)
        for item in cookies:
            # always opt in
            data[item] = self.request.cookie_settings.get(item) or CookieToggle.OFF
        return data

    def get_future_date(self, days):
        date = datetime.datetime.now() + datetime.timedelta(days=days)
        date = datetime.datetime.replace(date, hour=0, minute=0, second=0)
        return datetime.datetime.strftime(date, "%a, %d-%b-%Y %H:%M:%S GMT")

    def form_valid(self, form):
        response = super().form_valid(form)
        data = form.cleaned_data
        expires = self.get_future_date(days=settings.COOKIE_SETTINGS_EXPIRY)
        response.set_cookie("cookie_settings", json.dumps(data), expires=expires)
        return response
