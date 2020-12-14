from apps.core.interfaces import Barrier


def test_is_resolved_text__yes_with_date(barrier_data_1):
    barrier = Barrier(barrier_data_1)
    assert "Yes - December 2020" == barrier.is_resolved_text


def test_is_resolved_text__yes_without_date(barrier_data_1):
    data = barrier_data_1.copy()
    data.pop("status_date")
    barrier = Barrier(data)
    assert "Yes" == barrier.is_resolved_text


def test_status_date(barrier_data_1):
    barrier = Barrier(barrier_data_1)
    assert "2020-12-12 00:00:00" == str(barrier.status_date)


def test_is_resolved_text__no(barrier_data_1):
    data = barrier_data_1.copy()
    data["is_resolved"] = False
    barrier = Barrier(data)
    assert "No" == barrier.is_resolved_text


def test_country(barrier_data_1):
    barrier = Barrier(barrier_data_1)
    assert "Afghanistan" == barrier.country


def test_location(barrier_data_1):
    barrier = Barrier(barrier_data_1)
    assert "Afghanistan" == barrier.location


def test_simple_location__returns_country(barrier_data_5):
    barrier = Barrier(barrier_data_5)
    assert "Spain" == barrier.simple_location


def test_simple_location__fall_back_to_trading_block(barrier_data_5):
    """
    When there's no country for whatever reason, fall back to trading bloc
    """
    barrier_data_5["country"] = {}
    barrier = Barrier(barrier_data_5)
    assert "European Union" == barrier.simple_location


def test_last_published_on(barrier_data_1):
    barrier = Barrier(barrier_data_1)
    assert "2020-12-12 00:00:00" == str(barrier.last_published_on)


def test_reported_on(barrier_data_1):
    barrier = Barrier(barrier_data_1)
    assert "2020-12-01 00:00:00" == str(barrier.reported_on)


def test_categories_list(barrier_data_1):
    barrier = Barrier(barrier_data_1)
    assert ["Wibble", "Wobble"] == barrier.categories_list
