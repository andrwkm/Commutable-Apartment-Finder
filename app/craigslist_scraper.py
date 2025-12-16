from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import pandas as pd
import time


def setup_driver():
    # Docker container has Chrome pre-installed
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--start-maximized')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    print("WebDriver setup complete")
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

def search_terms(driver, terms):
    time.sleep(2)
    try:
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@enterkeyhint='search']"))
        )
        search_input.clear() #Clearing any text
        search_input.send_keys(terms)
        print(f"Searched for terms: {terms}")
    except:
        print("Could not enter search terms")

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
        
        print(f"Applied price filter: ${min_price} - ${max_price}")
        time.sleep(2)
        
    except:
        print("Could not apply price filter")

def apply_bedroom_filter(driver, min_bedrooms=None, max_bedrooms=None):
    if not min_bedrooms and not max_bedrooms:
        return

    try:
        if min_bedrooms:
            min_bed_input = driver.find_element(By.XPATH, "//input[@name='min_bedrooms']")
            min_bed_input.clear()
            min_bed_input.send_keys(str(min_bedrooms))

        if max_bedrooms:
            max_bed_input = driver.find_element(By.XPATH, "//input[@name='max_bedrooms']")
            max_bed_input.clear()
            max_bed_input.send_keys(str(max_bedrooms))

        print(f"Applied bedroom filter: {min_bedrooms} - {max_bedrooms}")

    except Exception as e:
        print("Could not apply bedroom filter:", e)

def apply_bathroom_filter(driver, min_bathrooms=None, max_bathrooms=None):
    if not min_bathrooms and not max_bathrooms:
        return

    try:
        if min_bathrooms:
            min_bath_input = driver.find_element(By.XPATH, "//input[@name='min_bathrooms']")
            min_bath_input.clear()
            min_bath_input.send_keys(str(min_bathrooms))

        if max_bathrooms:
            max_bath_input = driver.find_element(By.XPATH, "//input[@name='max_bathrooms']")
            max_bath_input.clear()
            max_bath_input.send_keys(str(max_bathrooms))

        print(f"Applied bathroom filter: {min_bathrooms} - {max_bathrooms}")

    except Exception as e:
        print("Could not apply bathroom filter:", e)

def apply_misc_filters(driver, cats_okay=False, dogs_okay=False, furnished=False, no_smoking=False, wheelchair_accessible=False, air_conditioning=False, ev_charging=False, no_application_fee=False, no_broker_fee=False):
    try:
        if cats_okay:
            cat_checkbox = driver.find_element(By.XPATH, "//input[@name='pets_cat']")
            if not cat_checkbox.is_selected():
                cat_checkbox.click()

        if dogs_okay:
            dog_checkbox = driver.find_element(By.XPATH, "//input[@name='pets_dog']")
            if not dog_checkbox.is_selected():
                dog_checkbox.click()

        if furnished:
            furnished_checkbox = driver.find_element(By.XPATH, "//input[@name='is_furnished']")
            if not furnished_checkbox.is_selected():
                furnished_checkbox.click()

        if no_smoking:
            no_smoking_checkbox = driver.find_element(By.XPATH, "//input[@name='no_smoking']")
            if not no_smoking_checkbox.is_selected():
                no_smoking_checkbox.click()

        if wheelchair_accessible:
            wheelchair_checkbox = driver.find_element(By.XPATH, "//input[@name='wheelchaccess']")
            if not wheelchair_checkbox.is_selected():
                wheelchair_checkbox.click()

        if air_conditioning:
            ac_checkbox = driver.find_element(By.XPATH, "//input[@name='airconditioning']")
            if not ac_checkbox.is_selected():
                ac_checkbox.click()

        if ev_charging:
            ev_checkbox = driver.find_element(By.XPATH, "//input[@name='ev_charging']")
            if not ev_checkbox.is_selected():
                ev_checkbox.click()

        if no_application_fee:
            no_app_fee_checkbox = driver.find_element(By.XPATH, "//input[@name='application_fee']")
            if not no_app_fee_checkbox.is_selected():
                no_app_fee_checkbox.click()

        if no_broker_fee:
            no_broker_fee_checkbox = driver.find_element(By.XPATH, "//input[@name='broker_fee']")
            if not no_broker_fee_checkbox.is_selected():
                no_broker_fee_checkbox.click()

        print("Applied miscellaneous filters")

    except Exception as e:
        print("Could not apply miscellaneous filters:", e)

def apply_laundry_filter(driver, wd_in_unit=False, wd_hookup=False, laundry_in_bldg=False, laundry_on_site=False, no_laundry=False):
    #if there is a true then click a button

    if not (wd_in_unit or wd_hookup or laundry_in_bldg or laundry_on_site or no_laundry):
        return
    
    try:
        filter_section = driver.find_elements(By.XPATH, "//button[@class='bd-button title link-like']")
        laundry_section = filter_section[2]
        laundry_section.click()

        laundry_elements = driver.find_elements(By.XPATH, "//input[@name='laundry']")

        if wd_in_unit:
            in_unit_checkbox = laundry_elements[0]
            if not in_unit_checkbox.is_selected():
                in_unit_checkbox.click()

        if wd_hookup:
            hookup_checkbox = laundry_elements[1]
            if not hookup_checkbox.is_selected():
                hookup_checkbox.click()

        if laundry_in_bldg:
            in_bldg_checkbox = laundry_elements[2]
            if not in_bldg_checkbox.is_selected():
                in_bldg_checkbox.click()

        if laundry_on_site:
            on_site_checkbox = laundry_elements[3]
            if not on_site_checkbox.is_selected():
                on_site_checkbox.click()

        if no_laundry:
            no_laundry_checkbox = laundry_elements[4]
            if not no_laundry_checkbox.is_selected():
                no_laundry_checkbox.click()

        print("Applied laundry filters")

    except Exception as e:
        print("Could not apply laundry filters:", e)


#combining all filters
def apply_all_filters(driver, terms="", min_price=None, max_price=None, 
                      min_bedrooms=None, max_bedrooms=None, 
                      min_bathrooms=None, max_bathrooms=None, 
                      cats_okay=False, dogs_okay=False, furnished=False, no_smoking=False, wheelchair_accessible=False, 
                      air_conditioning=False, ev_charging=False, no_application_fee=False, no_broker_fee=False, 
                      wd_in_unit=False, wd_hookup=False, laundry_in_bldg=False, laundry_on_site=False, no_laundry=False):
    
    search_terms(driver, terms)
    apply_price_filter(driver, min_price, max_price)
    apply_bedroom_filter(driver, min_bedrooms, max_bedrooms)
    apply_bathroom_filter(driver, min_bathrooms, max_bathrooms)
    apply_misc_filters(driver, cats_okay, dogs_okay, furnished, no_smoking, wheelchair_accessible, air_conditioning, ev_charging, no_application_fee, no_broker_fee)
    apply_laundry_filter(driver, wd_in_unit, wd_hookup, laundry_in_bldg, laundry_on_site, no_laundry)

    search_box = driver.find_element(By.XPATH, "//button[@class='bd-button icon-only cl-exec-search']") #searching and entering all filters
    search_box.click()



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
    total_listings = len(urls)
    counter = 0
    
    for target in urls:
        counter += 1
        print(f"Scraping data from listing {counter} of {total_listings}")
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


def scrape_craigslist(terms="",
                      min_price=None, max_price=None,
                      min_bedrooms=None, max_bedrooms=None,
                      min_bathrooms=None, max_bathrooms=None, 
                      cats_okay=False, dogs_okay=False, furnished=False, no_smoking=False, wheelchair_accessible=False, 
                      air_conditioning=False, ev_charging=False, no_application_fee=False, no_broker_fee=False, 
                      wd_in_unit=False, wd_hookup=False, laundry_in_bldg=False, laundry_on_site=False, no_laundry=False,
                      ):

    base_url = "https://newyork.craigslist.org/search/apa#search=2~gallery~0"
    
    driver = setup_driver()
    
    try:
        # Navigate to Craigslist
        driver.get(base_url)
        time.sleep(.5)
        
        # Apply filters
        switch_to_list_view(driver)
        apply_all_filters(driver, terms, min_price, max_price, 
                          min_bedrooms, max_bedrooms, 
                          min_bathrooms, max_bathrooms, 
                          cats_okay, dogs_okay, furnished, no_smoking, wheelchair_accessible, 
                          air_conditioning, ev_charging, no_application_fee, no_broker_fee, 
                          wd_in_unit, wd_hookup, laundry_in_bldg, laundry_on_site, no_laundry)
        
    
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
        
        print(df)

        return df
    
    finally: #stopping driver after scraping
        if driver:
            driver.quit()



if __name__ == "__main__":
    # TEST THE SCRAPER

    input_terms = input("Enter search terms (or leave blank): ")

    input_min_price = input("Enter minimum price (or leave blank): ")
    input_max_price = input("Enter maximum price (or leave blank): ")
    min_price = int(input_min_price) if input_min_price else None
    max_price = int(input_max_price) if input_max_price else None

    input_min_bedrooms = input("Enter minimum bedrooms (or leave blank): ")
    input_max_bedrooms = input("Enter maximum bedrooms (or leave blank): ")
    min_bedrooms = int(input_min_bedrooms) if input_min_bedrooms else None
    max_bedrooms = int(input_max_bedrooms) if input_max_bedrooms else None

    input_min_bathrooms = input("Enter minimum bathrooms (or leave blank): ")
    input_max_bathrooms = input("Enter maximum bathrooms (or leave blank): ")
    min_bathrooms = int(input_min_bathrooms) if input_min_bathrooms else None
    max_bathrooms = int(input_max_bathrooms) if input_max_bathrooms else None

    cats_okay = input("Allow cats? (y/n): ").lower() == 'y'
    dogs_okay = input("Allow dogs? (y/n): ").lower() == 'y'
    furnished = input("Furnished? (y/n): ").lower() == 'y'
    no_smoking = input("No smoking? (y/n): ").lower() == 'y'
    wheelchair_accessible = input("Wheelchair accessible? (y/n): ").lower() == 'y'
    air_conditioning = input("Air conditioning? (y/n): ").lower() == 'y'
    ev_charging = input("EV charging? (y/n): ").lower() == 'y'
    no_application_fee = input("No application fee? (y/n): ").lower() == 'y'
    no_broker_fee = input("No broker fee? (y/n): ").lower() == 'y'

    wd_in_unit = input("Washer/Dryer in unit? (y/n): ").lower() == 'y'
    wd_hookup = input("Washer/Dryer hookup? (y/n): ").lower() == 'y'
    laundry_in_bldg = input("Laundry in building? (y/n): ").lower() == 'y'
    laundry_on_site = input("Laundry on site? (y/n): ").lower() == 'y'
    no_laundry = input("No laundry? (y/n): ").lower() == 'y'


    
    # Example usage
    df = scrape_craigslist(terms=input_terms,
                           min_price=min_price, max_price=max_price,
                           min_bedrooms=min_bedrooms, max_bedrooms=max_bedrooms,
                           min_bathrooms=min_bathrooms, max_bathrooms=max_bathrooms,
                           cats_okay=cats_okay, dogs_okay=dogs_okay, furnished=furnished, no_smoking=no_smoking, wheelchair_accessible=wheelchair_accessible,
                           air_conditioning=air_conditioning, ev_charging=ev_charging, no_application_fee=no_application_fee, no_broker_fee=no_broker_fee,
                           wd_in_unit=wd_in_unit, wd_hookup=wd_hookup, laundry_in_bldg=laundry_in_bldg, laundry_on_site=laundry_on_site, no_laundry=no_laundry)

    print("\nResults:")
    print(df.head())
    