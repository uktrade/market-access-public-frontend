import pytest

from apps.core.interfaces import Barrier
from tests.metadata.fixtures import SectorFixtures, CountryFixtures, TradingBlocFixtures


@pytest.fixture
def barrier_data_1():
    return dummy_barrier_details(1)[0]

@pytest.fixture
def barrier_data_5():
    return dummy_barrier_details(5)[0]


def dummy_barrier_details(barrier_id=None):
    """ Data gateway always returns a list when S3 Select is used """
    return [
        b for b in dummy_barrier_list_results_raw if b["id"] == barrier_id
    ]


dummy_barrier_list_results_raw = [
    {
        "id": 1,
        "title": "Barrier 1",
        "summary": "Some summary",
        "is_resolved": True,
        "status_date": "2020-12-12",
        "country": CountryFixtures.afghanistan,
        "location": "Afghanistan",
        "sectors": [SectorFixtures.aerospace],
        "categories": [
            {"id": 1, "name": "Wibble"},
            {"id": 2, "name": "Wobble"},
        ],
        "trading_bloc": None,
        "last_published_on": "2020-12-12"
    },
    {
        "id": 2,
        "title": "Barrier 2",
        "country": CountryFixtures.afghanistan,
        "location": "Afghanistan",
        "sectors": [SectorFixtures.aerospace, SectorFixtures.water],
        "trading_bloc": None,
    },
    {
        "id": 3,
        "title": "Barrier 3",
        "country": CountryFixtures.nepal,
        "location": "Nepal",
        "sectors": [SectorFixtures.railways],
        "trading_bloc": None,
    },
    {
        "id": 4,
        "title": "Barrier 4",
        "country": CountryFixtures.brazil,
        "location": "Brazil",
        "sectors": [SectorFixtures.energy],
        "trading_bloc": None,
    },
    {
        "id": 5,
        "title": "Barrier 5",
        "country": CountryFixtures.spain,
        "location": "Spain",
        "sectors": [SectorFixtures.energy],
        "trading_bloc": TradingBlocFixtures.eu,
    },
]


dummy_barrier_list_results = [Barrier(item) for item in dummy_barrier_list_results_raw]
