import pytest

from splinter import Browser
from . import settings


@pytest.fixture(scope="module")
def browser():
    driver_name = settings.WEB_DRIVER_NAME
    attrs = {
        "driver_name": driver_name,
    }

    if settings.WEB_DRIVER_URL:
        attrs = {
            "driver_name": "remote",
            "browser": driver_name,
            "command_executor": settings.WEB_DRIVER_URL,
        }

    attrs["headless"] = settings.HEADLESS_MODE

    browser = Browser(**attrs)
    yield browser
    browser.quit()
