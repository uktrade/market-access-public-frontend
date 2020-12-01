class TradingBlocFixtures:
    eu = {
        "code": "TB00016",
        "name": "European Union",
        "short_name": "the EU",
    }


class CountryFixtures:
    afghanistan = {
        "id": "87756b9a-5d95-e211-a939-e4115bead28a",
        "name": "Afghanistan",
        "trading_bloc": None,
    }
    brazil = {
        "id": "b05f66a0-5d95-e211-a939-e4115bead28a",
        "name": "Brazil",
        "trading_bloc": None,
    }
    nepal = {
        "id": "1850bdb8-5d95-e211-a939-e4115bead28a",
        "name": "Nepal",
        "trading_bloc": None,
    }
    spain = {
        "id": "86756b9a-5d95-e211-a939-e4115bead28a",
        "name": "Spain",
        "overseas_region": {
            "name": "Europe",
            "id": "3e6809d6-89f6-4590-8458-1d0dab73ad1a",
        },
        "iso_alpha2_code": "ES",
        "trading_bloc": {"code": "TB00016", "name": "European Union"},
    }


class SectorFixtures:
    aerospace = {
        "id": "9538cecc-5f95-e211-a939-e4115bead28a",
        "name": "Aerospace",
    }
    energy = {
        "id": "b1959812-6095-e211-a939-e4115bead28a",
        "name": "Energy",
    }
    railways = {
        "id": "aa22c9d2-5f95-e211-a939-e4115bead28a",
        "name": "Railways",
    }
    water = {
        "id": "ae22c9d2-5f95-e211-a939-e4115bead28a",
        "name": "Water",
    }
