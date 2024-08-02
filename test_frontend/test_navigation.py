from playwright.sync_api import expect


def test_homepage(page, base_url):
    page.goto(base_url)
    expect(page.get_by_role("banner")).to_contain_text("Check International Trade Barriers")
    expect(page.locator("h1")).to_contain_text("What are you looking for?")


def test_find_unresolved_barrier_links(page, base_url):
    page.goto(base_url)
    page.get_by_role("link", name="Trade barriers", exact=True).click()
    expect(page.locator("#main-content")).to_contain_text(
        "Find trade barriers by location"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Find trade barriers by sector"
    )


def test_find_resolved_barrier_links(page, base_url):
    page.goto(base_url)
    page.get_by_role("link", name="Resolved trade barriers", exact=True).click()
    expect(page.locator("#main-content")).to_contain_text(
        "Find resolved trade barriers by location"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Find resolved trade barriers by sector"
    )


def test_find_trade_barrier_choose_location(page, base_url):
    page.goto(base_url)
    page.get_by_role("link", name="Trade barriers", exact=True).click()
    page.get_by_role("link", name="Find trade barriers by location").click()
    expect(page.locator("#main-content")).to_contain_text("Countries and territories")


def test_trade_barriers_in_all_locations(page, base_url):
    page.goto(base_url)
    page.get_by_role("link", name="Trade barriers", exact=True).click()
    page.get_by_role("link", name="Find trade barriers by location").click()
    page.get_by_role("link", name="Select all locations").click()
    expect(page.locator("#main-content")).to_contain_text("results found")


def test_resolved_trade_barriers(page, base_url):
    page.goto(base_url)
    page.get_by_role("link", name="Resolved trade barriers").click()
    page.get_by_role("link", name="Find resolved trade barriers by sector").click()
    page.get_by_role("link", name="Select all sectors").click()
    expect(page.locator("#main-content")).to_contain_text("results found")
