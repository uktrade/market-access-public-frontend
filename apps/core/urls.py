from django.urls import path
from django.views.generic import TemplateView

from .views import CookiesView, CookiePolicyView

app_name = "core"

urlpatterns = [
    path("cookies/", CookiesView.as_view(), name="cookies"),
    path("cookie-policy/", CookiePolicyView.as_view(), name="cookie-policy"),
    path('accessibility/', TemplateView.as_view(template_name="pages/accessibility.html"), name="accessibility"),
    path('disclaimer/', TemplateView.as_view(template_name="pages/disclaimer.html"), name="disclaimer"),
]
