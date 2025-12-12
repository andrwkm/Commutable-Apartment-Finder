from pandas import DataFrame

from app.craigslist_scraper import setup_driver, extract_preview_data, extract_detailed_data, scrape_craigslist

def test_driver_and_extraction():
    driver = setup_driver()

    assert driver is not None

    test_url = "https://newyork.craigslist.org/search/apa?min_bedrooms=4&query=apartment%20above#search=2~gallery~0"
    driver.get(test_url)

    preview_data = extract_preview_data(driver) #tuple of urls, prices, bedrooms

    assert isinstance(preview_data, tuple)

    assert len(preview_data) == 3 #urls, prices, bedrooms

    assert isinstance(preview_data[0], list) #url list
    assert isinstance(preview_data[1], list) #price list
    assert isinstance(preview_data[2], list) #bedrooms list

    assert len(preview_data[0]) == len(preview_data[1]) == len(preview_data[2]) #same lengths required

    #asserting types of data
    for url in preview_data[0]:
        assert isinstance(url, str)

    for price in preview_data[1]:
        assert isinstance(price, int)

    for beds in preview_data[2]:
        assert isinstance(beds, int)


    detailed_data = extract_detailed_data(driver, preview_data[0]) #inputting urls

    assert isinstance(detailed_data, tuple) #tuple of address, area, title

    assert len(detailed_data) == 3 #address, area, title
    assert isinstance(detailed_data[0], list) #address list
    assert isinstance(detailed_data[1], list) #area list
    assert isinstance(detailed_data[2], list) #title list

    assert len(detailed_data[0]) == len(detailed_data[1]) == len(detailed_data[2]) == len(preview_data[0]) #same lengths required and comparing it to url lengths

    #asserting types of data
    for address in detailed_data[0]:
        assert isinstance(address, str)
    for area in detailed_data[1]:
        assert isinstance(area, str)
    for title in detailed_data[2]:
        assert isinstance(title, str)

    driver.quit()



def test_scrape_craigslist_no_results():

    results_df = scrape_craigslist("mansion in new zealand with goats") #Should return 0 listings

    assert isinstance(results_df, DataFrame)

    assert results_df.empty
    
    assert "URL" in results_df.columns
    assert "Title" in results_df.columns
    assert "Address" in results_df.columns
    assert "Area" in results_df.columns
    assert "Bedrooms" in results_df.columns
    assert "Price" in results_df.columns


def test_scrape_craigslist():

    results_df = scrape_craigslist("really large in new york") #Should return 1-20 listings

    assert isinstance(results_df, DataFrame)

    assert len(results_df) > 0

    assert "URL" in results_df.columns
    assert "Title" in results_df.columns
    assert "Address" in results_df.columns
    assert "Area" in results_df.columns
    assert "Bedrooms" in results_df.columns
    assert "Price" in results_df.columns