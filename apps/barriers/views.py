from django.urls import reverse_lazy
from django.views.generic import TemplateView

from apps.core.metadata import countries


class FindBarriersSplashView(TemplateView):
    template_name = "barriers/find_barriers_splash.html"
    extra_context = {
        "title": "Find barriers"
    }

    def get_context_data(self, **kwargs):
        kwargs["location"] = self.request.GET.get("location")
        kwargs["sector"] = self.request.GET.get("sector")
        return super().get_context_data(**kwargs)


class LocationFiltersView(TemplateView):
    template_name = "barriers/choose_location.html"
    extra_context = {
        "breadcrumbs": (
            ("Choose a location", reverse_lazy("barriers:choose-location")),
        ),
        "countries": countries.grouped_alphabetically,
        "title": "Choose a location"
    }


class SectorFiltersView(TemplateView):
    template_name = "barriers/choose_sector.html"
    extra_context = {
        "breadcrumbs": (
            ("Choose a sector", reverse_lazy("barriers:choose-sector")),
        ),
        "title": "Choose a sector"
    }
