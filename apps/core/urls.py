from django.urls import path

from .views import CookiesView, CookiePolicyView

app_name = "core"

urlpatterns = [
    path("cookies/", CookiesView.as_view(), name="cookies"),
    path("cookie-policy/", CookiePolicyView.as_view(), name="cookie-policy"),
]