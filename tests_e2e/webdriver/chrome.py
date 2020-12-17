from splinter.driver.webdriver.chrome import WebDriver

from .mixins import NavigationMixin


class ChromeWebDriver(NavigationMixin, WebDriver):
    pass
