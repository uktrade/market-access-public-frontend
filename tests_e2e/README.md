# End to end tests for Market Access public frontend

This repository provides a set of end to end tests to ensure the core user journeys of the service is functional. 
 
#### Prerequisites
1. create a new virtual environment with (Python 3.7+)
2. activate the virtual environment then from project root run `pip install -r ./tests_e2e/requirements.txt`
3. (optional) install Chromedriver if you don't already have it then copy `chromedriver` to the virtual environment's bin folder that you just created

## Running E2E Tests
Please note that any host which is running the tests against an environment that is on VPN, will need to be connected to the same VPN as well.  
To run the tests:
1. activate the virtual environment
2. `cd tests_e2e` then run `pytest`
