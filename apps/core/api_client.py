import logging
from urllib.parse import urlencode, quote_plus

import requests
from django.conf import settings
from requests import HTTPError

from apps.core.interfaces import Barrier

logger = logging.getLogger(__name__)


class APIClient:

    def __init__(self):
        self.base_uri = settings.PUBLIC_API_GATEWAY_BASE_URI

    def get_base_uri(self):
        return self.base_uri or ""

    def uri(self, path):
        return f"{self.get_base_uri().rstrip('/')}/{path.lstrip('/')}"

    def request(self, method, uri, **kwargs):
        response = getattr(requests, method)(uri, **kwargs)
        try:
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            logger.exception(e)

    def filters_string(self, filters):
        filters_string = ""
        s3_filters = []

        if filters.get('id'):
            s3_filters.append(f"b.id = {filters['id']}")

        if filters.get('location'):
            s3_filters.append(f"b.country.name = '{filters['location']}'")

        if filters.get('sector'):
            s3_filters.append(f"'{filters['sector']}' IN b.sectors[*].name")

        if s3_filters:
            filters_string += "SELECT * FROM S3Object[*].barriers[*] AS b WHERE "
            filters_string += " AND ".join(s3_filters)
            filters_string = f"&query-s3-select={quote_plus(filters_string)}"

        return filters_string

    def get(self, uri, filters=None, **kwargs):
        # TODO: the api should not change contract when filters are applied
        uri += self.filters_string(filters)
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
        barriers = (Barrier(d) for d in barriers)
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
            raise HTTPError("Not found", response=self)


data_gateway = DataGatewayResource()
