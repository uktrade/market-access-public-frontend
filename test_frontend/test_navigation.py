from playwright.sync_api import expect

from .utils import clean_full_url


def test_find_resolved_barrier(page):
    page.goto("https://market-access-publicfe-gotham.london.cloudapps.digital/")
    page.get_by_role("heading", name="What are you looking for?").click()
    page.locator("p").filter(has_text="Trade barriers").nth(1).click()
    page.get_by_text("Current issues that may").click()
    page.locator("p").filter(has_text="Resolved trade barriers").click()
    page.get_by_text("Resolved issues which may").click()
    page.get_by_role("link", name="Trade barriers", exact=True).click()
    page.get_by_role("link", name="Find trade barriers by location").click()
    page.get_by_role("link", name="Anguilla (1)").click()
    page.get_by_role("link", name="test pub title").click()
    page.get_by_role("button", name="Back to search results").click()
    page.get_by_role("link", name="Home").click()


def test_find_by_location(page):
    page.goto("https://market-access-publicfe-gotham.london.cloudapps.digital/")
    page.get_by_role("link", name="Resolved trade barriers").click()
    page.get_by_role("link", name="Find resolved trade barriers by location").click()
    page.get_by_role("link", name="Home").click()


def test_two(page):
    page.goto("https://market-access-publicfe-gotham.london.cloudapps.digital/")
    page.get_by_role("link", name="Trade barriers", exact=True).click()
    page.get_by_role("link", name="Find trade barriers by sector").click()
    page.get_by_role("link", name="Advanced engineering (1)").click()
    page.get_by_role("link", name="uykyukuy").click()
    page.get_by_role("link", name="Home").click()
