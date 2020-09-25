import collections
import logging
from urllib.parse import quote_plus

import operator
import requests
from django.conf import settings
from django.http import Http404
from django.utils.text import slugify

from apps.core.interfaces import Barrier
from apps.core.utils import chain
from apps.metadata.aggregators import TradingBloc

logger = logging.getLogger(__name__)


class APIClient:

    def __init__(self):
        self.base_uri = settings.PUBLIC_API_GATEWAY_BASE_URI

    def get_base_uri(self):
        return self.base_uri or ""

    def uri(self, path):
        return f"{self.get_base_uri().rstrip('/')}/{path.lstrip('/')}"

    def request(self, method, uri, **kwargs):
        response = getattr(requests, method)(uri, timeout=5, **kwargs)
        try:
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            logger.exception(e)

    def s3_filters_string(self, filters):
        ignored_locations = ("All locations",)
        ignored_sectors = ("All sectors",)
        filters_string = ""
        s3_filters = []

        if filters.get('id'):
            s3_filters.append(f"b.id = {filters['id']}")
        else:
            # LOCATION filter
            location = filters.get('location')
            if location and location.name not in ignored_locations:
                if isinstance(location, TradingBloc):
                    # Trading Bloc
                    location_query_str = f"b.location LIKE '%{location.name}%'"
                else:
                    # Country
                    # Exact match
                    location_query_str = f"'{location.name}' = b.location"
                    # Country with trading bloc
                    location_query_str += f" OR b.location LIKE '%{location.name} (%'"
                s3_filters.append(f"( {location_query_str} )")

            if filters.get('sector') and filters.get('sector').name not in ignored_sectors:
                sectors_query_str = f"'{filters['sector']}' IN b.sectors[*].name"
                sectors_query_str += " OR 'All sectors' IN b.sectors[*].name"
                s3_filters.append(f"( {sectors_query_str} )")

            # IS_RESOLVED filter
            is_resolved = filters.get("is_resolved")
            if is_resolved is True:
                s3_filters.append("b.is_resolved = true")
            elif is_resolved is False:
                s3_filters.append("b.is_resolved = false")

        if s3_filters:
            filters_string += "SELECT * FROM S3Object[*].barriers[*] AS b WHERE "
            filters_string += " AND ".join(s3_filters)
            filters_string = f"&query-s3-select={quote_plus(filters_string)}"

        return filters_string

    def get(self, uri, filters=None, **kwargs):
        uri += self.s3_filters_string(filters)
        response = self.request("get", uri, **kwargs)
        data = response.json()
        # Worth noting that if filters are applied through query-s3-select
        # the API returns the data in "rows" key - instead of "barriers" key
        return data.get("rows") or data.get("barriers")


class DataGatewayResource(APIClient):

    def versioned_data_uri(self, version="latest", format="json"):
        data_path = f"{version}/data?format={format}"
        return self.uri(data_path)

    def barriers_list(self, version="latest", filters=None):
        uri = self.versioned_data_uri(version)
        barriers = self.get(uri, filters) or ()
        count = len(barriers)
        barriers = [Barrier(d) for d in barriers]

        # Apply ordering
        #   - sectors alphabetically trailed by barriers with "All sectors"
        #   - within each sector order records by location
        barriers_by_sector = {}

        for barrier in barriers:
            filtered_barriers = [b for b in barriers if b.sectors == barrier.sectors]
            filtered_barriers.sort(key=operator.attrgetter('location'))
            barriers_by_sector[slugify(barrier.sectors)] = filtered_barriers

        barriers_affecting_all_sectors = []
        try:
            barriers_affecting_all_sectors = barriers_by_sector.pop("all-sectors")
        except KeyError:
            # No records that would affect "All sectors"
            pass
        barriers_by_sector = collections.OrderedDict(sorted(barriers_by_sector.items()))

        barriers_affecting_specific_sectors = []
        for k, v in barriers_by_sector.items():
            barriers_affecting_specific_sectors += v

        barriers = chain(barriers_affecting_specific_sectors, barriers_affecting_all_sectors)

        data = {
            "all": barriers,
            "count": count
        }
        return data

    def barrier_details(self, version="latest", id=None):
        uri = self.versioned_data_uri(version)
        filters = {"id": id}
        barriers = self.get(uri, filters) or ()
        try:
            return Barrier(barriers[0])
        except (IndexError, TypeError):
            raise Http404("Barrier does not exist")


data_gateway = DataGatewayResource()
