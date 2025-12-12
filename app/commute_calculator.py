import googlemaps
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def get_gmaps_client(): #setting up gmaps client
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY not found.")
    
    return googlemaps.Client(key=api_key)


def calculate_commute_time(origin, destination, mode="transit"):
    gmaps = get_gmaps_client()
    
    try:
        #feeding distance matrix api with parameters
        result = gmaps.distance_matrix(
            origins=[origin],
            destinations=destination,
            mode=mode,
            departure_time=datetime.now()
        )
        
        element = result['rows'][0]['elements'][0] #extracting first element from results of distance matrix
        
        if element['status'] == 'OK': #if data is valid
            return {
                'duration_text': element['duration']['text'], #formatted text duration
                'duration_minutes': element['duration']['value'] / 60, #duration in minutes (used to filter later on)
                'distance_text': element['distance']['text'], #formatted text distance no need for value (no filtering done on distance)
            }
        else:
            return None

    except Exception as e:
        print(f"Commute API request failed for {origin}: {e}")
        return None


def add_commute_times(df, destination, mode="transit"):
    df = df.copy()
    
    commute_durations = [] #list holding string formatted durations
    commute_duration_minutes = [] #list holding float durations in minutes
    commute_distances = []
    
    for idx, row in df.iterrows(): #going through each row of inputted df
        origin = row.get("Address") or row.get("Area") #try address first then area
        
        if not origin: #if both are missing
            print(f"Row {idx}: No location data available.")
            commute_durations.append(None)
            commute_duration_minutes.append(None)
            commute_distances.append(None)
            continue
        
        commute = calculate_commute_time(origin, destination, mode)
        
        if commute:
            commute_durations.append(commute['duration_text'])
            commute_duration_minutes.append(commute['duration_minutes'])
            commute_distances.append(commute['distance_text'])
        else:
            commute_durations.append(None)
            commute_duration_minutes.append(None)
            commute_distances.append(None)
            

    df[f'Commute_Time_{mode}'] = commute_durations
    df[f'Commute_Minutes_{mode}'] = commute_duration_minutes
    df[f'Commute_Distance_{mode}'] = commute_distances
    
    return df


if __name__ == "__main__":
    
    choice = input("Would you like to run a commute time test? (y/n): ").lower()
    if choice == 'y':
        number_of_addresses = int(input("Enter number of test addresses to input: "))

        test_urls = []
        addresses = []
        areas = []
        titles = []
        bedrooms = []
        prices = []

        for i in range(number_of_addresses):
            

            url = f"URL {i+1}"
            Title = f"Listing {i+1}"
            address = input(f"Enter address {i+1} (leave blank if none): ")
            area = input(f"Enter area {i+1}): ")
            bedrooms = int(input(f"Enter number of bedrooms for listing {i+1}: "))
            price = int(input(f"Enter price for listing {i+1}: "))

            test_urls.append(url)
            titles.append(Title)
            addresses.append(address)
            areas.append(area)
            bedrooms.append(bedrooms)
            prices.append(price)

        df = pd.DataFrame({
            "URL": test_urls,
            "Title": titles,
            "Address": addresses,
            "Area": areas,
            "Bedrooms": bedrooms,
            "Price": prices
        })
    else:
        df = pd.DataFrame({
                "URL": ["example 1", "example 2"],
                "Title": ["Test1", "Test2"],
                "Address": ["270 Greenwich St, New York, NY 10007", ""],
                "Area": ["West Village", "185 Greenwich St Suite LL2365, New York, NY 10007"],
                "Bedrooms": [2, 1],
                "Price": [3000, 2500]
            })
        
    print(df[['URL', 'Area', 'Address']])
    
    DESTINATION_ADDRESS = input("Enter your work address or office: ")
    TRANSPORTATION_MODE = input("Enter transportation mode (driving, walking, bicycling, transit): ")

    try:
        df_with_commutes = add_commute_times(df, destination=DESTINATION_ADDRESS, mode=TRANSPORTATION_MODE)
        
        pd.set_option('display.max_columns', None)
        print(df_with_commutes)

    except ValueError as e:
        print("Please ensure GOOGLE_MAPS_API_KEY is correct")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")