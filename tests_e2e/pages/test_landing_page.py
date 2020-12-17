def test_landing_page__title(browser):
    browser.navigate("/")
    assert (
        "What are you looking for? - Check International Trade Barriers - GOV.UK"
        == browser.title
    )


def test_landing_page__main_heading(browser):
    browser.navigate("/")
    main_heading = browser.find_by_css(".govuk-heading-xl").first
    assert "What are you looking for?" == main_heading.text


def test_landing_page__trade_barriers_link(browser):
    browser.navigate("/")
    link_href = "/active/"
    link_text = "Trade barriers"

    active_link = browser.links.find_by_partial_href(link_href)

    assert active_link, f"Cannot find a link with href `{link_href}`"
    assert link_text == active_link.text, f"Cannot find link with `{link_text}`"


def test_landing_page__resolved_trade_barriers_link(browser):
    browser.navigate("/")
    link_href = "/resolved/"
    link_text = "Resolved trade barriers"

    resolved_link = browser.links.find_by_partial_href(link_href)

    assert resolved_link, f"Cannot find a link with href `{link_href}`"
    assert link_text == resolved_link.text, f"Cannot find link with `{link_text}`"
