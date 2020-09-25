from django.urls import reverse
from django.views.generic import TemplateView

from apps.core.api_client import data_gateway
from apps.core.mixins import BreadcrumbsMixin
from apps.metadata.aggregators import countries, sectors, AllSectors, trading_blocs


class BarriersListMixin:

    def get_barriers_list(self):
        filters = {
            "location": self.request.location,
            "sector": self.request.sector,
            "is_resolved": self.request.resolved,
        }
        response = data_gateway.barriers_list(filters=filters)
        return response


class FindBarriersSplashView(TemplateView):
    template_name = "barriers/find_barriers_splash.html"
    extra_context = {
        "title": "What are you looking for?"
    }


class FindActiveBarriers(BreadcrumbsMixin, TemplateView):
    template_name = "barriers/find_active_barriers.html"
    breadcrumbs = (("Find trade barriers", None),)
    extra_context = {
        "title": "Find trade barriers"
    }


class FindResolvedBarriers(BreadcrumbsMixin, TemplateView):
    template_name = "barriers/find_resolved_barriers.html"
    breadcrumbs = (("Find resolved trade barriers", None),)
    extra_context = {
        "title": "Find resolved trade barriers"
    }


class LocationFiltersView(BreadcrumbsMixin, BarriersListMixin, TemplateView):
    template_name = "barriers/choose_location.html"

    def get_breadcrumbs(self):
        if self.request.resolved:
            return (
                ("Find resolved trade barriers", reverse("barriers:find-resolved-barriers")),
                ("Choose a location", None),
            )
        return (("Choose a location", None),)

    def get_trading_blocs(self):
        barriers = self.get_barriers_list()
        choices = trading_blocs.count_records(
            "location", barriers["all"], op="include"
        )
        return choices

    def get_countries(self):
        barriers = self.get_barriers_list()
        choices = countries.count_records("country", barriers["all"])
        return choices

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trading_blocs"] = self.get_trading_blocs()
        context["countries"] = self.get_countries()
        context["title"] = "Choose a location"
        context["resolved"] = self.request.resolved
        return context


class SectorFiltersView(BreadcrumbsMixin, BarriersListMixin, TemplateView):
    template_name = "barriers/choose_sector.html"

    def get_breadcrumbs(self):
        if self.request.resolved:
            return (
                ("Find resolved trade barriers", reverse("barriers:find-resolved-barriers")),
                ("Choose a sector", None),
            )
        return (("Choose a sector", None),)

    def get_sectors(self):
        barriers = self.get_barriers_list()
        data = list(barriers["all"])
        all_sectors_count = len([b for b in data if b.sectors == AllSectors.name])
        choices = sectors.count_records(
            "sectors", data, op="include", offset=all_sectors_count
        )
        return choices

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sectors"] = self.get_sectors()
        context["title"] = "Choose a sector"
        return context


class BarriersListView(BreadcrumbsMixin, BarriersListMixin, TemplateView):
    template_name = "barriers/list.html"

    def get_title(self, location=None):
        if self.request.resolved:
            title = "Resolved trade barriers"
        else:
            title = "Trade barriers"
        if location and location != "all":
            title += f" in {location}"
        return title

    def get_breadcrumbs(self):
        if self.request.resolved:
            return (
                ("Find resolved trade barriers", reverse("barriers:find-resolved-barriers")),
                (self.get_title(self.request.location), None),
            )
        return ((self.get_title(self.request.location), None),)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["barriers"] = self.get_barriers_list()
        context["title"] = self.get_title(self.request.location)
        context["resolved"] = self.request.resolved
        return context


class BarrierDetailsView(TemplateView):
    template_name = "barriers/details.html"
    barrier = None

    def fetch_barrier(self, _id):
        self.barrier = data_gateway.barrier_details(id=_id)

    def get_search_title(self):
        title = "Trade barriers"
        if self.request.location and self.request.location != "all":
            title += f" in {self.request.location}"
        return title

    def get_breadcrumbs(self):
        return (
            (
                self.get_search_title(),
                reverse("barriers:list") + f"?{self.request.query_string}"
            ),
            (
                self.barrier.title,
                reverse(
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
