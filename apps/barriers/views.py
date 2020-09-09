from django.urls import reverse_lazy
from django.views.generic import TemplateView

from apps.core.api_client import data_gateway
from apps.metadata.aggregators import countries, sectors


class FindBarriersSplashView(TemplateView):
    template_name = "barriers/find_barriers_splash.html"
    extra_context = {
        "title": "Find barriers"
    }


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
        "sectors": sectors.grouped_alphabetically,
        "title": "Choose a sector"
    }


class BarriersListView(TemplateView):
    template_name = "barriers/list.html"

    def get_title(self, location=None):
        title = "Barriers"
        if location and location != "all":
            title += f" in {location}"
        return title

    def get_breadcrumbs(self):
        return (
            (
                self.get_title(self.request.location),
                reverse_lazy("barriers:list") + f"?{self.request.query_string}"
            ),
        )

    def get_barriers_list(self):
        filters = {
            "location": self.request.location,
            "sector": self.request.sector
        }
        response = data_gateway.barriers_list(filters=filters)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["barriers"] = self.get_barriers_list()
        context["breadcrumbs"] = self.get_breadcrumbs()
        context["title"] = self.get_title(self.request.location)
        return context


class BarrierDetailsView(TemplateView):
    template_name = "barriers/details.html"
    barrier = None

    def fetch_barrier(self, _id):
        self.barrier = data_gateway.barrier_details(id=_id)

    def get_search_title(self):
        title = "Barriers"
        if self.request.location and self.request.location != "all":
            title += f" in {self.request.location}"
        return title

    def get_breadcrumbs(self):
        return (
            (
                self.get_search_title(),
                reverse_lazy("barriers:list") + f"?{self.request.query_string}"
            ),
            (
                self.barrier.title,
                reverse_lazy(
                    "barriers:details",
                    kwargs={"barrier_id": self.barrier.id}
                ) + f"?{self.request.query_string}"
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.fetch_barrier(context["barrier_id"])
        context["title"] = self.barrier.title
        context["barrier"] = self.barrier
        context["breadcrumbs"] = self.get_breadcrumbs()
        return context
