from http import HTTPStatus
from urllib.parse import quote_plus

from django.http import Http404, HttpResponse
from django.test import TestCase
from mock import patch, Mock
from requests import Response, HTTPError

from apps.core.api_client import APIClient, data_gateway
from apps.metadata.aggregators import countries, trading_blocs, sectors
from tests.barriers.fixtures import (
    dummy_barrier_list_results,
    dummy_barrier_list_results_raw,
    dummy_barrier_details,
)
from tests.core.helpers import mocked_requests_get


class DummyResource(APIClient):
    pass


class APIClientTestCase(TestCase):
    def setUp(self):
        self.base_uri = "https://dummy.api/"
        self.resource = DummyResource(base_uri=self.base_uri)

    def test_base_uri(self):
        assert self.base_uri == self.resource.base_uri

    def test_uri(self):
        path = "heyho/"
        expected_uri = "https://dummy.api/heyho/"
        assert expected_uri == self.resource.uri(path)

    def test_uri__path_with_leading_slash(self):
        path = "/heyho/"
        expected_uri = "https://dummy.api/heyho/"
        assert expected_uri == self.resource.uri(path)

    def test_s3_filters_string__id(self):
        filters = {"id": 123}
        expected_sql = "SELECT * FROM S3Object[*].barriers[*] AS b WHERE b.id = 123"
        expected_query_string = f"&query-s3-select={quote_plus(expected_sql)}"

        assert expected_query_string == self.resource.s3_filters_string(filters)

    def test_s3_filters_string__id_takes_precedence(self):
        filters = {"id": 123, "location": countries.es}
        expected_sql = "SELECT * FROM S3Object[*].barriers[*] AS b WHERE b.id = 123"
        expected_query_string = f"&query-s3-select={quote_plus(expected_sql)}"

        assert expected_query_string == self.resource.s3_filters_string(filters)

    def test_s3_filters_string__location_trading_bloc(self):
        filters = {"location": trading_blocs.eu}
        expected_sql = "SELECT * FROM S3Object[*].barriers[*] AS b WHERE ( b.location = 'European Union' )"
        expected_query_string = f"&query-s3-select={quote_plus(expected_sql)}"

        assert expected_query_string == self.resource.s3_filters_string(filters)

    def test_s3_filters_string__location_country_wo_trading_bloc(self):
        """
        Countries without trading block are simply matched to the location name
        """
        filters = {"location": countries.au}
        expected_sql = "SELECT * FROM S3Object[*].barriers[*] AS b WHERE ( b.location = 'Australia' )"
        expected_query_string = f"&query-s3-select={quote_plus(expected_sql)}"

        assert expected_query_string == self.resource.s3_filters_string(filters)

    def test_s3_filters_string__location_country(self):
        """
        Countries with a trading block will contain extra filters to ensure
        trading block wide records are included
        """
        filters = {"location": countries.es}
        expected_sql = (
            "SELECT * FROM S3Object[*].barriers[*] AS b "
            "WHERE ( b.location = 'Spain'"
            " OR b.location LIKE '%Spain (%'"
            " OR b.location = 'European Union' )"
        )
        expected_query_string = f"&query-s3-select={quote_plus(expected_sql)}"

        assert expected_query_string == self.resource.s3_filters_string(filters)

    def test_s3_filters_string__sector(self):
        filters = {"sector": sectors.chemicals}
        expected_sql = (
            "SELECT * FROM S3Object[*].barriers[*] AS b "
            "WHERE ( 'Chemicals' IN b.sectors[*].name"
            " OR 'All sectors' IN b.sectors[*].name )"
        )
        expected_query_string = f"&query-s3-select={quote_plus(expected_sql)}"

        assert expected_query_string == self.resource.s3_filters_string(filters)

    def test_s3_filters_string__is_resolved_true(self):
        filters = {"is_resolved": True}
        expected_sql = (
            "SELECT * FROM S3Object[*].barriers[*] AS b " "WHERE b.is_resolved = true"
        )
        expected_query_string = f"&query-s3-select={quote_plus(expected_sql)}"

        assert expected_query_string == self.resource.s3_filters_string(filters)

    def test_s3_filters_string__is_resolved_false(self):
        filters = {"is_resolved": False}
        expected_sql = (
            "SELECT * FROM S3Object[*].barriers[*] AS b " "WHERE b.is_resolved = false"
        )
        expected_query_string = f"&query-s3-select={quote_plus(expected_sql)}"

        assert expected_query_string == self.resource.s3_filters_string(filters)

    def test_s3_filters_string__all(self):
        filters = {
            "location": countries.au,
            "sector": sectors.chemicals,
            "is_resolved": True,
        }
        expected_sql = (
            "SELECT * FROM S3Object[*].barriers[*] AS b "
            "WHERE ( b.location = 'Australia' )"
            " AND ( 'Chemicals' IN b.sectors[*].name OR 'All sectors' IN b.sectors[*].name )"
            " AND b.is_resolved = true"
        )
        expected_query_string = f"&query-s3-select={quote_plus(expected_sql)}"

        assert expected_query_string == self.resource.s3_filters_string(filters)

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_get__s3select_rows(self, _mock_get):
        """ Should return "rows" from the response if it's an s3 select response """
        uri = self.resource.uri("heyho-data")
        r = self.resource.get(uri, {"id": 1})
        assert r

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_get__barriers_without_filters(self, _mock_get):
        """ Should return "barriers" from the response if s3 select was not involved """
        uri = self.resource.uri("heyho-data")
        r = self.resource.get(uri)
        assert r

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_get_raises_HTTPError(self, _mock_get):
        """ Should return "barriers" from the response if s3 select was n ot involved """
        with self.assertRaises(HTTPError):
            self.resource.get("ahoy")


class DataGatewayTestCase(TestCase):
    def test_sorted_by_location(self):
        barriers = dummy_barrier_list_results
        expected_order = [1, 2, 4, 3, 5]

        assert expected_order == [
            item.id for item in data_gateway.sort_by_location(barriers)
        ]

    def test_sorted_by_sectors(self):
        barriers = dummy_barrier_list_results
        expected_order = [1, 2, 4, 5, 3]

        assert expected_order == [
            item.id for item in data_gateway.sort_by_sectors(barriers)
        ]

    @patch("apps.core.api_client.APIClient.get")
    def test_barriers_list(self, mock_get):
        mock_get.return_value = dummy_barrier_list_results_raw
        expected_count = len(dummy_barrier_list_results_raw)
        data = data_gateway.barriers_list()

        assert "all" in data.keys()
        assert expected_count == data["count"]

    @patch("apps.core.api_client.APIClient.get")
    def test_barrier_details(self, mock_get):
        barrier_id = 3
        mock_get.return_value = dummy_barrier_details(barrier_id)
        expected_public_id = f"PID-{barrier_id}"
        barrier = data_gateway.barrier_details(id=barrier_id)

        assert expected_public_id == barrier.public_id

    @patch("apps.core.api_client.APIClient.get")
    def test_barrier_details_404(self, mock_get):
        barrier_id = "something-non-existent"
        mock_get.return_value = dummy_barrier_details(barrier_id)

        with self.assertRaisesMessage(Http404, "Barrier does not exist"):
            data_gateway.barrier_details(id=barrier_id)
