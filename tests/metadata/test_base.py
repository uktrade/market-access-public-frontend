from django.test import TestCase

from apps.metadata.base import metadata


class MetadataTestCase(TestCase):

    def test_get_admin_area_by_id(self):
        admin_area_id = "b5d03d97-fef5-4da6-9117-98a4d633b581"   # Acre (Brazil)
        expected_name = "Acre"
        expected_country_name = "Brazil"

        admin_area = metadata.get_admin_area(admin_area_id)

        assert admin_area_id == admin_area["id"]
        assert expected_name == admin_area["name"]
        assert expected_country_name == admin_area["country"]["name"]

    def test_get_admin_areas_by_ids__using_list_as_param(self):
        admin_area_id_1 = "b5d03d97-fef5-4da6-9117-98a4d633b581"  # Acre (Brazil)
        admin_area_id_2 = "539aacb1-9778-4db9-b992-7be49b7503d7"  # Adygea (Russia)

        admin_areas = metadata.get_admin_areas((admin_area_id_1, admin_area_id_2))

        assert 2 == len(admin_areas)
        assert {admin_area_id_1, admin_area_id_2} == set([aa["id"] for aa in admin_areas])

    def test_get_admin_areas_by_ids__using_str_as_param(self):
        admin_area_id_1 = "b5d03d97-fef5-4da6-9117-98a4d633b581"  # Acre (Brazil)
        admin_area_id_2 = "539aacb1-9778-4db9-b992-7be49b7503d7"  # Adygea (Russia)
        admin_area_ids = f"{admin_area_id_1}, {admin_area_id_2}"

        admin_areas = metadata.get_admin_areas((admin_area_ids))

        assert 2 == len(admin_areas)
        assert {admin_area_id_1, admin_area_id_2} == set([aa["id"] for aa in admin_areas])

    def test_get_country_by_id(self):
        country_id = "aa5f66a0-5d95-e211-a939-e4115bead28a"  #  Bermuda
        expected_country_name = "Bermuda"
        expected_iso_alpha2_code = "BM"

        country = metadata.get_country(country_id)

        assert expected_country_name == country["name"]
        assert expected_iso_alpha2_code == country["iso_alpha2_code"]

    def test_get_sector_by_id(self):
        sector_id = "9538cecc-5f95-e211-a939-e4115bead28a"  #  Aerospace
        expected_sector_name = "Aerospace"

        sector = metadata.get_sector(sector_id)

        assert expected_sector_name == sector["name"]

    def test_sectors_by_ids__using_list_as_param(self):
        sector_id_1 = "9538cecc-5f95-e211-a939-e4115bead28a"  #  Aerospace
        sector_id_2 = "aa38cecc-5f95-e211-a939-e4115bead28a"  #  Maritime

        sectors = list(metadata.get_sectors((sector_id_1, sector_id_2)))

        assert 2 == len(sectors)
        assert {sector_id_1, sector_id_2} == set(s["id"] for s in sectors)

    def test_sectors_by_ids__using_str_as_param(self):
        sector_id_1 = "9538cecc-5f95-e211-a939-e4115bead28a"  # Aerospace
        sector_id_2 = "aa38cecc-5f95-e211-a939-e4115bead28a"  # Maritime
        sector_ids = f"{sector_id_1}, {sector_id_2}"

        sectors = list(metadata.get_sectors(sector_ids))

        assert 2 == len(sectors)
        assert {sector_id_1, sector_id_2} == set(s["id"] for s in sectors)
