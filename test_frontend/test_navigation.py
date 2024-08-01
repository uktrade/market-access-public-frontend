from playwright.sync_api import expect


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
