import pytest

from .browser import get_browser


@pytest.fixture(scope="module")
def browser():
    browser = get_browser()
    yield browser
    browser.quit()
