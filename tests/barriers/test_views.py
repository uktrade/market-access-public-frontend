from http import HTTPStatus

from django.test import TestCase
from django.urls import resolve, reverse
from mock import patch

from apps.barriers.views import LocationFiltersView, SectorFiltersView, BarriersListView, BarrierDetailsView
from tests.core.helpers import mocked_requests_get


class LocationFiltersViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("barriers:choose-location")

    def test_location_url_resolves_to_correct_view(self):
        match = resolve("/location/")
        assert match.func.view_class == LocationFiltersView

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_location_view_loads_correct_template(self, _mock_get):
        url = f"{self.url}?sector=aerospace"
        response = self.client.get(url)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, "barriers/choose_location.html")

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_location_breadcrumbs__with_resolved_barriers(self, _mock_get):
        url = f"{self.url}?resolved=1"
        response = self.client.get(url)

        assert HTTPStatus.OK == response.status_code

        breadcrumbs = response.context_data["breadcrumbs"]
        assert 2 == len(breadcrumbs)
        assert ("Find resolved trade barriers", '/resolved/') == breadcrumbs[0]
        assert ("Choose a location", None) == breadcrumbs[1]

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_location_breadcrumbs__with_active_barriers(self, _mock_get):
        url = f"{self.url}?resolved=0"
        response = self.client.get(url)

        assert HTTPStatus.OK == response.status_code

        breadcrumbs = response.context_data["breadcrumbs"]
        assert 2 == len(breadcrumbs)
        assert ("Find active trade barriers", '/active/') == breadcrumbs[0]
        assert ("Choose a location", None) == breadcrumbs[1]

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_location_breadcrumbs__no_query_params(self, _mock_get):
        url = f"{self.url}"
        response = self.client.get(url)

        assert HTTPStatus.OK == response.status_code

        breadcrumbs = response.context_data["breadcrumbs"]
        assert 2 == len(breadcrumbs)
        assert ("Find active trade barriers", '/active/') == breadcrumbs[0]
        assert ("Choose a location", None) == breadcrumbs[1]


class SectorFiltersViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("barriers:choose-sector")

    def test_sector_url_resolves_to_correct_view(self):
        match = resolve("/sector/")
        assert match.func.view_class == SectorFiltersView

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_sector_view_loads_correct_template(self, _mock_get):
        url = f"{self.url}"
        response = self.client.get(url)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, "barriers/choose_sector.html")

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_sector_breadcrumbs__with_resolved_barriers(self, _mock_get):
        url = f"{self.url}?resolved=1"
        response = self.client.get(url)

        assert HTTPStatus.OK == response.status_code

        breadcrumbs = response.context_data["breadcrumbs"]
        assert 2 == len(breadcrumbs)
        assert ("Find resolved trade barriers", '/resolved/') == breadcrumbs[0]
        assert ("Choose a sector", None) == breadcrumbs[1]

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_sector_breadcrumbs__with_active_barriers(self, _mock_get):
        url = f"{self.url}?resolved=0"
        response = self.client.get(url)

        assert HTTPStatus.OK == response.status_code

        breadcrumbs = response.context_data["breadcrumbs"]
        assert 2 == len(breadcrumbs)
        assert ("Find active trade barriers", '/active/') == breadcrumbs[0]
        assert ("Choose a sector", None) == breadcrumbs[1]

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_sector_breadcrumbs__no_query_params(self, _mock_get):
        url = f"{self.url}"
        response = self.client.get(url)

        assert HTTPStatus.OK == response.status_code

        breadcrumbs = response.context_data["breadcrumbs"]
        assert 2 == len(breadcrumbs)
        assert ("Find active trade barriers", '/active/') == breadcrumbs[0]
        assert ("Choose a sector", None) == breadcrumbs[1]


class BarriersListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("barriers:list")

    def test_barriers_url_resolves_to_correct_view(self):
        match = resolve("/barriers/")
        assert match.func.view_class == BarriersListView

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_barriers_list_view_loads_correct_template(self, _mock_get):
        response = self.client.get(self.url)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, "barriers/list.html")

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_barrier_list_context__with_active_filter(self, _mock_get):
        url = f"{self.url}?resolved=0"
        response = self.client.get(url)
        assert HTTPStatus.OK == response.status_code
        assert "Active trade barriers" == response.context_data["title"]
        breadcrumbs = response.context_data["breadcrumbs"]
        assert 2 == len(breadcrumbs)
        assert ("Find active trade barriers", '/active/') == breadcrumbs[0]
        assert ("Active trade barriers", None) == breadcrumbs[1]

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_barrier_list_context__with_resolved_filter(self, _mock_get):
        url = f"{self.url}?resolved=1"
        response = self.client.get(url)

        assert HTTPStatus.OK == response.status_code
        assert "Resolved trade barriers" == response.context_data["title"]
        breadcrumbs = response.context_data["breadcrumbs"]
        assert 2 == len(breadcrumbs)
        assert ("Find resolved trade barriers", '/resolved/') == breadcrumbs[0]
        assert ("Resolved trade barriers", None) == breadcrumbs[1]

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_barrier_list_context__without_filter(self, _mock_get):
        response = self.client.get(self.url)
        assert HTTPStatus.OK == response.status_code
        assert "Active trade barriers" == response.context_data["title"]
        breadcrumbs = response.context_data["breadcrumbs"]
        assert 2 == len(breadcrumbs)
        assert ("Find active trade barriers", '/active/') == breadcrumbs[0]
        assert ("Active trade barriers", None) == breadcrumbs[1]

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_barrier_list_title__with_location_filter(self, _mock_get):
        url = f"{self.url}?location=es"
        response = self.client.get(url)
        assert HTTPStatus.OK == response.status_code
        assert "Active trade barriers in Spain" == response.context_data["title"]

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_barrier_list_title__with_location_filter__all(self, _mock_get):
        url = f"{self.url}?location=all"
        response = self.client.get(url)
        assert HTTPStatus.OK == response.status_code
        assert "Active trade barriers in All locations" == response.context_data["title"]


class BarrierDetailsViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse("barriers:details", kwargs={"barrier_id": 1})

    def test_barrier_details_url_resolves_to_correct_view(self):
        match = resolve("/barriers/1/")
        assert match.func.view_class == BarrierDetailsView

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_barrier_details_view_loads_correct_template(self, _mock_get):
        response = self.client.get(self.url)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, "barriers/details.html")

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_barrier_details_context__with_active_filter(self, _mock_get):
        url = f"{self.url}?resolved=0"
        response = self.client.get(url)

        assert HTTPStatus.OK == response.status_code
        assert "Barrier 1" == response.context_data["title"]
        breadcrumbs = response.context_data["breadcrumbs"]
        assert 3 == len(breadcrumbs)
        assert ("Find active trade barriers", '/active/') == breadcrumbs[0]
        assert ("Active trade barriers", '/barriers/?resolved=0') == breadcrumbs[1]
        assert ("Barrier 1", None) == breadcrumbs[2]

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_barrier_details_context__with_resolved_filter(self, _mock_get):
        url = f"{self.url}?resolved=1"
        response = self.client.get(url)

        assert HTTPStatus.OK == response.status_code
        assert "Barrier 1" == response.context_data["title"]
        breadcrumbs = response.context_data["breadcrumbs"]
        assert 3 == len(breadcrumbs)
        assert ("Find resolved trade barriers", '/resolved/') == breadcrumbs[0]
        assert ("Resolved trade barriers", '/barriers/?resolved=1') == breadcrumbs[1]
        assert ("Barrier 1", None) == breadcrumbs[2]

    @patch("requests.get", side_effect=mocked_requests_get)
    def test_barrier_list_context__without_filter(self, _mock_get):
        response = self.client.get(self.url)
        assert HTTPStatus.OK == response.status_code
        assert "Barrier 1" == response.context_data["title"]
        breadcrumbs = response.context_data["breadcrumbs"]
        assert 3 == len(breadcrumbs)
        assert ("Find active trade barriers", '/active/') == breadcrumbs[0]
        assert ("Active trade barriers", '/barriers/?') == breadcrumbs[1]
        assert ("Barrier 1", None) == breadcrumbs[2]
