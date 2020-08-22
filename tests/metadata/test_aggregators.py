from django.test import TestCase

from apps.metadata.aggregators import countries, sectors


class CountriesAggregatorTestCase(TestCase):

    def test_countries(self):
        count = len(countries.all)
        assert 218 == count

    def test_empty_admin_areas(self):
        admin_areas = countries.spain.admin_areas
        assert not admin_areas

    def test_admin_areas(self):
        admin_areas = countries.brazil.admin_areas
        expected_admin_areas_count = 27

        assert admin_areas
        assert expected_admin_areas_count == len(admin_areas.all)

    def test_country_attributes(self):
        germany = countries.de
        assert germany.id
        assert "Germany" == germany.name
        assert germany.iso_alpha2_code


class SectorsAggregatorTestCase(TestCase):

    def test_sectors(self):
        assert 44 == len(sectors.all)

    def test_sector_attributes(self):
        aerospace = sectors.aerospace
        assert aerospace.id
        assert "Aerospace" == aerospace.name
