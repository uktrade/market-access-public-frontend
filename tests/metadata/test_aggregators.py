from django.test import TestCase

from apps.metadata.aggregators import (AdminArea, AllLocations, AllSectors,
                                       Country, Sector, TradingBloc,
                                       TradingBlocsAggregator, countries,
                                       sectors, trading_blocs)
from apps.metadata.base import metadata
from tests.barriers.fixtures import dummy_barrier_list_results


class AdminAreaTestCase(TestCase):
    def test_admin_area_attributes(self):
        brazil = countries.br
        acre = brazil.admin_areas.acre
        assert isinstance(acre, AdminArea)
        assert "<AdminArea - Acre>" == repr(acre)
        assert "Acre" == str(acre)
        assert "Acre" == acre.name
        assert hasattr(acre, "disabled_on")
        assert acre.id


class CountriesAggregatorTestCase(TestCase):
    def test_countries(self):
        count = len(countries.all)
        assert 218 == count

    def test_empty_admin_areas(self):
        # Spain does not have admin areas
        admin_areas = countries.es.admin_areas
        assert not admin_areas

    def test_admin_areas(self):
        # Brazil has admin areas
        admin_areas = countries.br.admin_areas
        expected_admin_areas_count = 27

        assert admin_areas
        assert expected_admin_areas_count == len(admin_areas.all)

    def test_country_attributes(self):
        germany = countries.de
        assert isinstance(germany, Country)
        assert "<Country - Germany>" == repr(germany)
        assert "Germany" == str(germany)
        assert "Germany" == germany.name
        assert "DE" == germany.iso_alpha2_code
        assert "de" == germany.slug
        assert germany.id

    def test_count_records(self):
        """
        Used to help to display how many records each country has at location
        filter.
        """
        dataset = dummy_barrier_list_results
        grouped_records = countries.count_records("country", dataset)
        # it is grouped and ordered alphabetically
        afghanistan = grouped_records["A"][0]
        assert countries.af == afghanistan
        assert 2 == afghanistan.records_count
        assert 2 == len([b for b in dataset if b.country == afghanistan.name])


class AllLocationsTestCase(TestCase):
    def test_all_locations_attributes(self):
        all_locations = AllLocations()
        assert "<AllLocations - All locations>" == repr(all_locations)
        assert "All locations" == str(all_locations)
        assert "All locations" == all_locations.name


class SectorsAggregatorTestCase(TestCase):
    def test_sectors(self):
        assert 26 == len(sectors.all)

    def test_sector_attributes(self):
        aerospace = sectors.aerospace
        assert isinstance(aerospace, Sector)
        assert "<Sector - Aerospace>" == repr(aerospace)
        assert "Aerospace" == str(aerospace)
        assert "Aerospace" == aerospace.name
        assert "aerospace" == aerospace.slug
        assert aerospace.id

    def test_sector_slug(self):
        sector = sectors.advanced_engineering
        assert "advanced-engineering" == sector.slug

    def test_all_sectors_attributes(self):
        all_sectors = AllSectors()
        assert "<AllSectors - All sectors>" == repr(all_sectors)
        assert "All sectors" == str(all_sectors)
        assert "All sectors" == all_sectors.name

    def test_count_records(self):
        """
        Used to help to display how many records each sector has at sectors
        filter.
        """
        dataset = dummy_barrier_list_results
        grouped_records = sectors.count_records("sectors", dataset, op="include")
        # it is grouped and ordered alphabetically
        aerospace = grouped_records["A"][1]
        assert "Aerospace" == aerospace.name
        assert 2 == aerospace.records_count
        assert 2 == len([b for b in dataset if aerospace.name in b.sectors])

    def test_count_records__with_offset(self):
        """
        Used to help to display how many records each sector has at sectors
        filter.
        Offset is used to add an amount to the counted records.
        """
        offset = 2
        dataset = dummy_barrier_list_results
        grouped_records = sectors.count_records(
            "sectors", dataset, op="include", offset=offset
        )
        # it is grouped and ordered alphabetically
        aerospace = grouped_records["A"][1]
        assert "Aerospace" == aerospace.name
        assert 2 == len([b for b in dataset if aerospace.name in b.sectors])
        assert 2 + offset == aerospace.records_count

    def test_count_records__exact_match(self):
        """
        Used to help to display how many records each sector has at sectors
        filter.
        """
        dataset = dummy_barrier_list_results
        grouped_records = sectors.count_records("sectors", dataset)
        # it is grouped and ordered alphabetically
        aerospace = grouped_records["A"][1]
        assert "Aerospace" == aerospace.name
        # There are 2 records with aerospace listed in sectors
        assert 2 == len([b for b in dataset if aerospace.name in b.sectors])
        # However, there's only 1 record with ONLY aerospace listed in sectors
        assert 1 == aerospace.records_count


class TradingBlocsAggregatorTestCase(TestCase):
    def test_trading_blocs(self):
        count = len(trading_blocs.all)
        assert 1 == count

    def test_trading_bloc_attributes(self):
        eu = trading_blocs.eu
        assert isinstance(eu, TradingBloc)
        assert "TB00016" == eu.code
        assert "European Union" == eu.name
        assert "the EU" == eu.short_name
        assert "European Union" == str(eu)
        assert "<TradingBloc - European Union>" == repr(eu)
        assert "EU" == eu.iso_alpha2_code
        assert "eu" == eu.slug
        assert eu.country_iso_codes
        assert eu.members

    def test_trading_bloc_members_are_countries(self):
        eu = trading_blocs.eu
        member = list(eu.members)[0]

        assert isinstance(member, Country)

    def test_trading_block_raises_attr_error(self):
        """
        In case the trading block has an iso_alpha2_code that:
         - does not belong to a country (check spelling?)
         - has not been added to the countries list in metadata.json
        """
        invalid_iso_alpha2_code = "w1bl3"
        error_msg = (
            f"'CountriesAggregator' object has no attribute '{invalid_iso_alpha2_code}'"
        )

        with self.assertRaisesMessage(AttributeError, error_msg):
            data = metadata.get_trading_bloc_list()
            data[0]["country_iso_codes"].append(invalid_iso_alpha2_code)
            _trading_blocs = TradingBlocsAggregator(
                TradingBloc, data, attr_from="iso_alpha2_code"
            )
