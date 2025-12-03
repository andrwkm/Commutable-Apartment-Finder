from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import pandas as pd
import time


def setup_driver():

    #Autoinstaller code snippet found from: https://stackoverflow.com/questions/67626049/how-to-add-chromedriver-to-my-github-repository
    chromedriver_autoinstaller.install()
    
    #Chrome driver options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    
    return driver


def switch_to_list_view(driver): #Switching to list view on Craigslist
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='bd-button icon-only cl-search-view-mode-list']")
            )
        )
        driver.execute_script("arguments[0].click();", button)
        print("Switched to list view")
    except:
        print("Could not switch to list view")


#Apply price filter to Craigslist search
def apply_price_filter(driver, min_price=None, max_price=None):
    if not min_price and not max_price:
        return

    try:
        input_price_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='range-inputs']"))
        )
        
        min_price_input = input_price_elements[0].find_element(By.XPATH, "//input[@placeholder='min']")
        max_price_input = input_price_elements[0].find_element(By.XPATH, "//input[@placeholder='max']")
        
        if min_price:
            min_price_input.clear()
            min_price_input.send_keys(str(min_price))
        
        if max_price:
            max_price_input.clear()
            max_price_input.send_keys(str(max_price))
            max_price_input.send_keys(u'\ue007')
        
        print(f"Applied price filter: ${min_price} - ${max_price}")
        time.sleep(2)
        
    except:
        print("Could not apply price filter")


def extract_preview_data(driver):
    try:
    # wait until at least one listing is present, then grab all listings
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='result-data']")))
        listing_elements = driver.find_elements(By.XPATH, "//div[@class='result-data']")
    except Exception as e:
        print("No listings found:", e)
        listing_elements = []
    
    print(f"Found {len(listing_elements)} listings")
    
    urls = []
    prices = []
    bedrooms = []
    
    for listing in listing_elements:
        # URL
        try:
            link_element = listing.find_elements(By.TAG_NAME, 'a')
            urls.append(link_element[0].get_attribute("href") if link_element else "")
        except:
            urls.append("")
        
        # Price
        try:
            price_element = listing.find_element(By.CLASS_NAME, 'priceinfo')
            prices.append(price_element.text)
        except:
            prices.append("")
        
        # Bedrooms
        try:
            bedrooms_element = listing.find_element(By.CLASS_NAME, 'post-bedrooms')
            bedroom_count = int(bedrooms_element.text.replace('br', ''))
            bedrooms.append(bedroom_count)
        except:
            bedrooms.append("")
    
    return urls, prices, bedrooms

def extract_detailed_data(driver, urls):
    address = []
    area = []
    title = []
    
    for target in urls:
        driver.get(target) #navigate to each listing
        time.sleep(.5)
        try:
            #address
            address_element = driver.find_element(By.CLASS_NAME, 'street-address')
            address.append(address_element.text)
        except:
            address.append("")


        try:
            #area (for api to search if no address is given)
            spans = driver.find_elements(By.CSS_SELECTOR, ".postingtitletext span")

            found = False
            for s in spans:
                text = s.text.strip()
                if text.startswith("(") and text.endswith(")"):
                    text = text[1:-1]  # Remove the parentheses
                    area.append(text)
                    found = True
                    break  #exit loop once the area is found
            if not found:
                area.append("")
            
        except:
            area.append("")

        try:
            #title
            title_element = driver.find_element(By.ID, 'titletextonly')
            title.append(title_element.text)
        except:
            title.append("")
        
    return address, area, title


def scrape_craigslist(min_price=None, max_price=None, min_bedrooms=None, max_bedrooms=None):

    base_url = "https://newyork.craigslist.org/search/apa#search=2~gallery~0"
    
    driver = setup_driver()
    
    try:
        # Navigate to Craigslist
        driver.get(base_url)
        time.sleep(2)
        
        # Apply filters
        switch_to_list_view(driver)
        apply_price_filter(driver, min_price, max_price)
        
        # Extract preview data
        urls, prices, bedrooms = extract_preview_data(driver)
        
        
        addresses, areas, titles = extract_detailed_data(driver, urls)
        
        # Build DataFrame
        df = pd.DataFrame({
            "URL": urls,
            "Title": titles,
            "Address": addresses,
            "Area": areas,
            "Bedrooms": bedrooms,
            "Price": prices
        })
        
        return df
        
    finally: #stopping driver after scraping
        if driver:
            driver.quit()


if __name__ == "__main__":
    # TEST THE SCRAPER
    
    input_min_price = input("Enter minimum price (or leave blank): ")
    input_max_price = input("Enter maximum price (or leave blank): ")
    min_price = int(input_min_price) if input_min_price else None
    max_price = int(input_max_price) if input_max_price else None

    input_min_bedrooms = input("Enter minimum bedrooms (or leave blank): ")
    input_max_bedrooms = input("Enter maximum bedrooms (or leave blank): ")
    min_bedrooms = int(input_min_bedrooms) if input_min_bedrooms else None
    max_bedrooms = int(input_max_bedrooms) if input_max_bedrooms else None
    
    # Example usage
    df = scrape_craigslist(
        min_price=min_price,
        max_price=max_price,
        min_bedrooms=min_bedrooms,
        max_bedrooms=max_bedrooms,
    )
    
    print("\nResults:")
    print(df.head())
    