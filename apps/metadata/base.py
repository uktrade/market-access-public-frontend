import json

from django.conf import settings


class Metadata:
    """
    Wrapper around the raw metadata with helper functions
    """

    def __init__(self, data):
        self.data = data

    def get_admin_area(self, admin_area_id):
        for admin_area in self.data["country_admin_areas"]:
            if admin_area["id"] == admin_area_id and admin_area["disabled_on"] is None:
                return admin_area

    def get_admin_areas(self, admin_area_ids):
        """
        Helper to get admin areas data in bulk.

        :param admin_area_ids: either a list or a comma separated string of UUIDs
        :return: GENERATOR - data of admin areas
        """
        area_ids = admin_area_ids or []
        if type(area_ids) == str:
            area_ids = admin_area_ids.replace(" ", "").split(",")
        admin_areas = [self.get_admin_area(area_id) for area_id in area_ids]
        return admin_areas

    def get_admin_areas_by_country(self, country_id):
        return [
            admin_area
            for admin_area in self.data["country_admin_areas"]
            if admin_area["country"]["id"] == country_id
        ]

    def get_country(self, country_id):
        for country in self.data["countries"]:
            if country["id"] == country_id:
                return country

    def get_location_text(self, country_id, admin_area_ids):
        country_data = self.get_country(country_id)

        if country_data:
            country_name = country_data["name"]
        else:
            country_name = ""

        if admin_area_ids:
            admin_areas_string = ", ".join(
                [
                    self.get_admin_area(admin_area_id)["name"]
                    for admin_area_id in admin_area_ids
                ]
            )
            return f"{admin_areas_string} ({country_name})"

        return country_name

    def get_country_list(self):
        return self.data["countries"]

    def get_sector(self, sector_id):
        for sector in self.data.get("sectors", []):
            if sector["id"] == sector_id:
                return sector

    def get_sectors(self, sector_ids):
        """
        Helper to get sectors data in bulk.

        :param sector_ids: either a list or a comma separated string of UUIDs
        :return: GENERATOR - data of sectors
        """
        sec_ids = sector_ids or []
        if type(sec_ids) == str:
            sec_ids = sector_ids.replace(" ", "").split(",")
        sectors = (self.get_sector(sector_id) for sector_id in sec_ids)
        return sectors

    def get_sectors_by_ids(self, sector_ids):
        return [
            sector
            for sector in self.data.get("sectors", [])
            if sector["id"] in sector_ids and sector["disabled_on"] is None
        ]

    def get_sector_list(self, level=None):
        return [
            sector
            for sector in self.data["sectors"]
            if (level is None or sector["level"] == level)
            and sector["disabled_on"] is None
        ]


def get_metadata():
    file = f"{settings.ROOT_DIR}/apps/core/fixtures/metadata.json"
    with open(file) as f:
        return Metadata(json.load(f))


metadata = get_metadata()
