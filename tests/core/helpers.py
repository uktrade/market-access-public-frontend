import requests

from tests.barriers.fixtures import dummy_barrier_list_results_raw


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if 400 <= self.status_code <= 599:
                raise requests.exceptions.HTTPError

    if "query-s3-select" in args[0]:
        return MockResponse({"rows": dummy_barrier_list_results_raw}, 200)
    elif "dummy.api" in args[0]:
        return MockResponse({"barriers": dummy_barrier_list_results_raw}, 200)

    return MockResponse(None, 404)
