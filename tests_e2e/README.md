# End to end tests for Market Access public frontend

This repository provides a set of end to end tests to ensure the core user journeys of the service are functional.

#### Prerequisites
1. create a new virtual environment with (Python 3.9+)
2. activate the virtual environment then from project root run `pip install -r ./tests_e2e/requirements.txt`
3. (optional) install Chromedriver if you don't already have it
4. copy `chromedriver` to the virtual environment's bin folder that you just created

## Running E2E Tests
Please note that any host which is running the tests against an environment that is on VPN, will need to be connected to the same VPN as well.

To run the tests do:
1. ensure the app on http://localhost:9980/ is available
Note: you may want to run the tests against another instance, in that case adjust the `BASE_URL` in `./tests_e2e/settings.py`
2. activate the virtual environment
3. from project root `cd tests_e2e` then run `pytest`
