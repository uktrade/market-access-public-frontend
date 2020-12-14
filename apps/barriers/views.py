from django.urls import reverse
from django.views.generic import TemplateView

from apps.core.api_client import data_gateway
from apps.core.mixins import BreadcrumbsMixin
from apps.metadata.aggregators import (
    countries,
    sectors,
    AllSectors,
    AllLocations,
    trading_blocs,
)


class BarriersListMixin:
    _barriers = None

    def get_sort_field(self):
        """
        Get sort field based on filters currently applied:

                       -------------Location-------------
                       |___None___|__Value___|___All____|
               | None  | location | sectors  | location |
        Sector | Value | location | location | location |
               | All   | location | sectors  | location |
        """
        if self.request.location is not None and not isinstance(
            self.request.location, AllLocations
        ):
            if self.request.sector is None or isinstance(
                self.request.sector, AllSectors
            ):
                return "sectors"
        return "location"

    def get_barriers_list(self):
        if not self._barriers:
            filters = {
                "location": self.request.location,
                "sector": self.request.sector,
                "is_resolved": self.request.resolved,
            }
            self._barriers = data_gateway.barriers_list(
                filters=filters,
                sort_by=self.get_sort_field(),
                headers=self.request.zipkin_http_headers,
            )
        return self._barriers

    def get_visible_groups(self, groups):
        """
        Helper to list the group letters that have records and so it's easier to
        show/hide them in the templates. (i.e on the sector/location pages)
        """
        visible_groups = []
        for k, v in groups.items():
            items_with_records = [item for item in v if item.records_count]
            if items_with_records:
                visible_groups.append(k)
        return visible_groups


class FindBarriersSplashView(TemplateView):
    template_name = "barriers/find_barriers_splash.html"
    extra_context = {
        "title": "What are you looking for?",
    }


class FindActiveBarriers(BreadcrumbsMixin, TemplateView):
    template_name = "barriers/find_active_barriers.html"
    breadcrumbs = (("Find trade barriers", None),)
    extra_context = {
        "title": "Find trade barriers",
    }


class FindResolvedBarriers(BreadcrumbsMixin, TemplateView):
    template_name = "barriers/find_resolved_barriers.html"
    breadcrumbs = (("Find resolved trade barriers", None),)
    extra_context = {
        "title": "Find resolved trade barriers",
    }


class LocationFiltersView(BreadcrumbsMixin, BarriersListMixin, TemplateView):
    template_name = "barriers/choose_location.html"

    def get_breadcrumbs(self):
        if self.request.resolved:
            return (
                (
                    "Find resolved trade barriers",
                    reverse("barriers:find-resolved-barriers"),
                ),
                ("Choose a location", None),
            )
        return (
            ("Find trade barriers", reverse("barriers:find-active-barriers")),
            ("Choose a location", None),
        )

    def get_trading_blocs(self):
        barriers = self.get_barriers_list()
        choices = trading_blocs.count_records("trading_bloc", barriers["all"])
        return choices

    def get_countries(self):
        barriers = self.get_barriers_list()
        choices = countries.count_records("country", barriers["all"])
        return choices

    def get_caption(self):
        caption = ""
        if self.request.sector:
            caption = f"in {self.request.sector.name}"
        return caption

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trading_blocs"] = self.get_trading_blocs()
        context["trading_blocs_with_records"] = self.get_visible_groups(
            context["trading_blocs"]
        )
        context["countries"] = self.get_countries()
        context["countries_with_records"] = self.get_visible_groups(
            context["countries"]
        )
        context["title"] = "Choose a location"
        context["caption"] = self.get_caption()
        context["resolved"] = self.request.resolved
        return context


class SectorFiltersView(BreadcrumbsMixin, BarriersListMixin, TemplateView):
    template_name = "barriers/choose_sector.html"

    def get_breadcrumbs(self):
        if self.request.resolved:
            return (
                (
                    "Find resolved trade barriers",
                    reverse("barriers:find-resolved-barriers"),
                ),
                ("Choose a sector", None),
            )
        return (
            ("Find trade barriers", reverse("barriers:find-active-barriers")),
            ("Choose a sector", None),
        )

    def get_sectors(self):
        barriers = self.get_barriers_list()
        data = list(barriers["all"])
        all_sectors_count = len([b for b in data if b.sectors == AllSectors.name])
        choices = sectors.count_records(
            "sectors", data, op="include", offset=all_sectors_count
        )
        return choices

    def get_caption(self):
        caption = ""
        if self.request.location:
            caption = f"in {self.request.location.name}"
        return caption

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sectors"] = self.get_sectors()
        context["sectors_with_records"] = self.get_visible_groups(context["sectors"])
        context["title"] = "Choose a sector"
        context["caption"] = self.get_caption()
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
                (
                    "Find resolved trade barriers",
                    reverse("barriers:find-resolved-barriers"),
                ),
                ("Resolved trade barriers", None),
            )
        return (
            ("Find trade barriers", reverse("barriers:find-active-barriers")),
            ("Trade barriers", None),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["barriers"] = self.get_barriers_list()
        context["title"] = self.get_title(self.request.location)
        return context


class BarrierDetailsView(BreadcrumbsMixin, TemplateView):
    template_name = "barriers/details.html"
    barrier = None

    def get(self, request, *args, **kwargs):
        self.barrier = data_gateway.barrier_details(
            id=self.kwargs["barrier_id"],
            headers=self.request.zipkin_http_headers,
        )
        return super().get(request, *args, **kwargs)

    def get_breadcrumbs(self):
        if self.request.resolved:
            return (
                (
                    "Find resolved trade barriers",
                    reverse("barriers:find-resolved-barriers"),
                ),
                (
                    "Resolved trade barriers",
                    reverse("barriers:list") + f"?{self.request.query_string}",
                ),
                (self.barrier.title, None),
            )
        return (
            ("Find trade barriers", reverse("barriers:find-active-barriers")),
            (
                "Trade barriers",
                reverse("barriers:list") + f"?{self.request.query_string}",
            ),
            (self.barrier.title, None),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.barrier.title
        context["barrier"] = self.barrier
        return context
