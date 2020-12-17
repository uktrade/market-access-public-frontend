from splinter.browser import get_driver
from splinter.exceptions import DriverNotFoundError

from . import settings
from .webdriver.chrome import ChromeWebDriver


_DRIVERS = {
    "chrome": ChromeWebDriver,
}


def get_browser():
    """
    Wrapper to get the selenium driver.
    """
    driver = None
    driver_name = settings.WEB_DRIVER_NAME

    try:
        driver = _DRIVERS[driver_name]
    except KeyError:
        raise DriverNotFoundError("No driver for %s" % driver_name)

    attrs = {
        "headless": settings.HEADLESS_MODE,
    }

    return get_driver(driver, **attrs)
