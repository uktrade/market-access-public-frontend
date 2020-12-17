def test_check_details_of_a_trade_barrier(browser):
    """
    Case 1 - Full journey for trade barriers
    1.  go to index page "What are you looking for?" then select "Trade barriers"
        expected: land on Find trade barriers page
    2.  select "Find trade barriers by location"
        expected: land on find trade barriers by location
    3.  select any location with barriers
        expected: page lands in on results page "Trade barriers in <country>"
    4.  click on any Trade barrier
        expected: land on barrier page
    5.  click on back to results
        expected: back to results
    """

    # Step 1 - select trade barriers path
    browser.navigate("/")
    browser.links.find_by_partial_text("Trade barriers").click()
    # Check that the user lands on the right page
    main_heading = browser.find_by_css(".govuk-heading-xl").first
    assert "Find trade barriers" == main_heading.text

    # Step 2 - select search by location path
    browser.links.find_by_partial_text("Find trade barriers by location").click()
    # Check that the user lands on the right page
    main_heading = browser.find_by_css(".govuk-heading-xl").first
    assert "Choose a location" == main_heading.text

    # Step 3 - select a country in location filters
    country = browser.find_by_css(".country__item").first
    # Strip the record indicator e.g. " (2)"
    country_name = "".join(country.text.split(" ")[:-1])
    country.click()
    # Check that the user lands on the right page
    main_heading = browser.find_by_css(".govuk-heading-xl").first
    assert f"Trade barriers in {country_name}" == main_heading.text

    # Step 4 - select a barrier from search results
    barrier = browser.find_by_css(".barrier__item").first
    barrier_title = barrier.text
    barrier.click()
    # Check that the user lands on the right page
    main_heading = browser.find_by_css(".govuk-heading-xl").first
    assert barrier_title == main_heading.text

    # Step 5 - back to search results
    button = browser.find_by_css(".back-to-search-results__button").first
    assert "Back to search results" == button.text.strip()
    button.click()
    # Check that the user lands on the right page
    main_heading = browser.find_by_css(".govuk-heading-xl").first
    assert f"Trade barriers in {country_name}" == main_heading.text


def test_check_details_of_a_resolved_trade_barrier(browser):
    """
    Case 2 - Full journey for resolved trade barriers
    1.  go to index page "What are you looking for?" then select "Resolved trade barriers"
        expected: land on Find trade barriers page
    2.  select "Find resolved trade barriers by location"
        expected: land on find resolved trade barriers by location
    3.  select any location with barriers
        expected: page lands on results page "Resolved trade barriers in <country>"
    4.  click on any Trade barrier
        expected: land on barrier page
    5.  click on back to results
        expected: back to results
    """

    # Step 1 - select resolved trade barriers path
    browser.navigate("/")
    browser.links.find_by_partial_text("Resolved trade barriers").click()
    # Check that the user lands on the right page
    main_heading = browser.find_by_css(".govuk-heading-xl").first
    assert "Find resolved trade barriers" == main_heading.text

    # Step 2 - select search by location path
    browser.links.find_by_partial_text(
        "Find resolved trade barriers by location"
    ).click()
    # Check that the user lands on the right page
    main_heading = browser.find_by_css(".govuk-heading-xl").first
    assert "Choose a location" == main_heading.text

    # Step 3 - select a country in location filters
    country = browser.find_by_css(".country__item").first
    # Strip the record indicator e.g. " (2)"
    country_name = "".join(country.text.split(" ")[:-1])
    country.click()
    # Check that the user lands on the right page
    main_heading = browser.find_by_css(".govuk-heading-xl").first
    assert f"Resolved trade barriers in {country_name}" == main_heading.text

    # Step 4 - select a barrier from search results
    barrier = browser.find_by_css(".barrier__item").first
    barrier_title = barrier.text
    barrier.click()
    # Check that the user lands on the right page
    main_heading = browser.find_by_css(".govuk-heading-xl").first
    assert barrier_title == main_heading.text

    # Step 5 - back to search results
    button = browser.find_by_css(".back-to-search-results__button").first
    assert "Back to search results" == button.text.strip()
    button.click()
    # Check that the user lands on the right page
    main_heading = browser.find_by_css(".govuk-heading-xl").first
    assert f"Resolved trade barriers in {country_name}" == main_heading.text
