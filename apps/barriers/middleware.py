from urllib.parse import parse_qs, urlencode

from django.utils.deprecation import MiddlewareMixin

from apps.core.utils import convert_to_snake_case
from apps.metadata.aggregators import countries, sectors, AllLocations, AllSectors, trading_blocs


class FiltersMiddleware(MiddlewareMixin):
    def process_request(self, request):  # noqa: C901
        """
        Add location and sector from the uri to request
        so the selection is available across the views
        """
        request.location = None
        request.sector = None
        request.next = None
        request.resolved = None
        request.query_string = request.META.get("QUERY_STRING")
        params = parse_qs(request.query_string)

        if "location" in params:
            location = params["location"][0]
            if location == "all":
                request.location = AllLocations()
            elif location == "eu":
                request.location = trading_blocs.eu
            else:
                request.location = getattr(countries, params["location"][0])

        if "sector" in params:
            sector_name = convert_to_snake_case(params["sector"][0])
            if sector_name == "all":
                request.sector = AllSectors()
            else:
                request.sector = getattr(sectors, sector_name)

        if "next" in params:
            next = params.pop("next")[0]
            query_params = urlencode(params, doseq=True)
            url = next
            if query_params:
                url += f"?{query_params}"
            request.next = url

        if "resolved" in params:
            resolved = params.pop("resolved")[0]
            if resolved == "1":
                request.resolved = True
            elif resolved == "0":
                request.resolved = False

    def process_response(self, request, response):
        return response
