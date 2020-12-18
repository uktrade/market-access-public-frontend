# Market Access Public Frontend 
[![CircleCI](https://circleci.com/gh/uktrade/market-access-public-frontend.svg?style=svg)](https://circleci.com/gh/uktrade/market-access-public-frontend)
[![Coverage Status](https://coveralls.io/repos/github/uktrade/market-access-public-frontend/badge.svg?branch=master)](https://coveralls.io/github/uktrade/market-access-public-frontend?branch=master)
[![E2E Tests](https://github.com/uktrade/market-access-public-frontend/workflows/E2E%20Tests/badge.svg)(https://github.com/uktrade/market-access-public-frontend/actions)

This repository provides a frontend client to consume public barrier data through the Data Gateway.
It's built with python django. 

## Installation with Docker

The project is using docker compose to setup and run all the necessary components. \
The docker-compose.yml file provided is meant to be used for running tests and development environments.
It has a gulp task runner to process and prepare assets like CSS and JS files. 

#### Prerequisites
1. Install `docker` & `docker compose` - https://docs.docker.com/install/
2. Make sure you have node v12.x installed - https://nodejs.org/en/
2. Clone the repository:
    ```shell
    git clone https://github.com/uktrade/market-access-public-frontend.git
    cd market-access-public-frontend
    ```

#### Install
1. Copy the env file - `cp dmas-pubfe.local-template.env dmas-pubfe.local.env`  
2. Build the images and spin up the containers by running - `docker-compose up --build`
3. (recommended) Set up git hooks by running - `make git-hooks`
4. (optional) Enter bash within the django container using `docker-compose exec web bash`
then create a superuser `py3 manage.py createsuperuser --email your@email.here` then `exit` the container
5. To start the dev server run - `make django-run`
6. The fronted client is now accessible via http://localhost:9980
7. run `make dev` - this will run the relevant gulp tasks (compile & watch CSS and JS files) and launch BrowserSync
8. run `make django-static` to generate the static files - for more info please refer to Staticfiles section below

##### BrowserSync auto-reload:
When you visit the site via http://localhost:9981 BrowserSync will automatically reload the page when you modify scss or js files.

#### Running in detached mode
The installation steps above will require 3 terminal windows to be open to run the processes.
If desired this can be reduced to 0 via the following commands:
1. Start the containers in detached mode - `docker-compose up -d`
2. Start django in detached mode - `make django-run-detached`
3. The frontend client is now accessible via http://market-access.local:9880

Now even if you closed your terminal, the server would be still running.
You only need to run the gulp tasks via `make dev` if you're planning to work with SCSS or JS files. 

#### Make commands
There's a set of make commands that you can utilize straight away. \
To list all available commands with help text type `make help` in terminal and hit `Enter`.

#### Staticfiles
The project is using CSS and fonts from `govuk-frontend` npm package.

Resources for GOV.UK Frontend:
- https://frontend.design-system.service.gov.uk/#gov-uk-frontend
- https://github.com/alphagov/govuk-frontend/tree/master/src/govuk

Fonts are copied while css is imported from node modules.
To prepare staticfiles for local run `make dev`

Staticfiles are compressed offline for most environments, so it makes sense that you could run the same way locally to test things out. 
To do that, just: 
1. stop the django development server (if it's running) 
2. set `DEBUG` to `False` in `config/settings/local.py`
3. run `npm run build` for a one off run (or `make dev` if you want to recompile css and js real time when changes are saved)
3. run `make django-static`
4. start the django development server

**Note:** this is a good way to mimic how files are generated and served in an environment, \
but please note, lazy loading of static files is also disabled in offline mode, so your changes to templates, js, scss \
might not take effect unless you run step 3 from above and restart your dev server.
To keep watching and recompiling css and js file use `make dev` from step 3. 

## Builds
Builds can be initiated from Jenkins or from the command line using `cf` CLI tool (using `cf push <app_name>`).
To use `cf push` you will need to be in the root of the project.

The preferred way to deploy apps remains Jenkins as of now because Jenkins will set environment variables as part of the flow.

#### Init Tasks
Tasks that should be run at app initialisation can be defined in `.profile` file.
If you would like to check the output of that you can do so via `cf logs <app_name> --recent`, but 
please note that these logs get trimmed so it's best to check straight after deployment. 

## Tests
Front end tests are grouped under `./test` directory. When writing tests please use the corresponding app name to keep the same folder structure as the main app so it's easy to tell which test belongs to which app.

#### Running Django Tests
The project's test runner is pytest - https://docs.pytest.org/en/latest/
1. You can run all or a subset of tests via `make django-test`, if you pass in a value in `path` then it will run that subset of tests.
Example usage.:
	- `make django-test` - run all tests
	- `make django-test path=barriers` - run a subset of tests just for the barriers app
	- `make django-test path=assessments/test_assessment_detail.py::EmptyAssessmentDetailTestCase::test_view` - run a specific test case
2. To run tests with coverage use `make django-test-coverage` - this will output the report to the console.

