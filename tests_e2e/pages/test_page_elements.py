from .. import settings


def test_footer_links__feedback(browser):
    browser.visit(settings.BASE_URL)
    path = "feedback/"
    link_text = "Feedback and issues"

    footer_links = browser.driver.find_elements_by_css_selector("footer a")
    link = [i for i in footer_links if i.text == link_text]

    assert link, f"Cannot find link with `{link_text}`"
    assert f"{settings.BASE_URL}{path}" == link[0].get_attribute("href")


def test_footer_links__disclaimer(browser):
    browser.visit(settings.BASE_URL)
    path = "disclaimer/"
    link_text = "Disclaimer"

    footer_links = browser.driver.find_elements_by_css_selector("footer a")
    link = [i for i in footer_links if i.text == link_text]

    assert link, f"Cannot find link with `{link_text}`"
    assert f"{settings.BASE_URL}{path}" == link[0].get_attribute("href")


def test_footer_links__accessibility(browser):
    browser.visit(settings.BASE_URL)
    path = "accessibility/"
    link_text = "Accessibility"

    footer_links = browser.driver.find_elements_by_css_selector("footer a")
    link = [i for i in footer_links if i.text == link_text]

    assert link, f"Cannot find link with `{link_text}`"
    assert f"{settings.BASE_URL}{path}" == link[0].get_attribute("href")


def test_footer_links__cookies(browser):
    browser.visit(settings.BASE_URL)
    path = "cookies/"
    link_text = "Cookies"

    footer_links = browser.driver.find_elements_by_css_selector("footer a")
    link = [i for i in footer_links if i.text == link_text]

    assert link, f"Cannot find link with `{link_text}`"
    assert f"{settings.BASE_URL}{path}" == link[0].get_attribute("href")


def test_common_links_on_results_page(browser):
    browser.visit(f"{settings.BASE_URL}barriers/?resolved=0")

    # Report a trade barrier
    rtb_text = "report a trade barrier"
    rtb_href = "https://www.great.gov.uk/report-trade-barrier/"
    rtb_link = browser.links.find_by_partial_href(rtb_href)
    assert rtb_link, f"Cannot find a link with href `{rtb_href}`"
    assert rtb_text == rtb_link.text, f"Cannot find link with `{rtb_text}`"

    # CHEG
    cheg_text = "check duties and customs procedures"
    cheg_href = "https://www.gov.uk/check-duties-customs-exporting"
    cheg_link = browser.links.find_by_partial_href(cheg_href)
    assert cheg_link, f"Cannot find a link with href `{cheg_href}`"
    assert cheg_text == cheg_link.text, f"Cannot find link with `{cheg_text}`"


def test_common_links_on_details_page(browser):
    browser.visit(f"{settings.BASE_URL}barriers/?resolved=0")
    barrier = browser.find_by_css(".barrier__item").first
    barrier_title = barrier.text
    barrier.click()

    # Step 1 - Check that the user lands on the right page
    main_heading = browser.find_by_css(".govuk-heading-xl").first
    assert barrier_title == main_heading.text

    # Step 2 - Check the links
    # Report a trade barrier
    rtb_text = "report a trade barrier"
    rtb_href = "https://www.great.gov.uk/report-trade-barrier/"
    rtb_link = browser.links.find_by_partial_href(rtb_href)
    assert rtb_link, f"Cannot find a link with href `{rtb_href}`"
    assert rtb_text == rtb_link.text, f"Cannot find link with `{rtb_text}`"

    # CHEG
    cheg_text = "check duties and customs procedures"
    cheg_href = "https://www.gov.uk/check-duties-customs-exporting"
    cheg_link = browser.links.find_by_partial_href(cheg_href)
    assert cheg_link, f"Cannot find a link with href `{cheg_href}`"
    assert cheg_text == cheg_link.text, f"Cannot find link with `{cheg_text}`"
