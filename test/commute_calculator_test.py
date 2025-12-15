from pandas import DataFrame
from app.commute_calculator import get_gmaps_client, calculate_commute_time, add_commute_times
from datetime import datetime

def test_get_gmaps_client():
    gmaps = get_gmaps_client()
    assert gmaps is not None


def test_calculate_commute_time():
    origin = "Penn Station, New York, NY"
    destination = "Times Square, New York, NY"
    commute = calculate_commute_time(origin, destination, mode="walking")

    assert commute is not None
    assert 'duration_text' in commute #checking if data exists
    assert 'duration_minutes' in commute
    assert 'distance_text' in commute

    #asserting data types
    assert isinstance(commute['duration_text'], str)
    assert isinstance(commute['duration_minutes'], float)
    assert isinstance(commute['distance_text'], str)

def test_add_commute_times():
    data = {
        "Address": ["Penn Station, New York, NY", "Grand Central Terminal, New York, NY"],
        "Area": ["Midtown", "Midtown"]
    }
    df = DataFrame(data)
    destination = "Times Square, New York, NY"
    
    result_df = add_commute_times(df, destination, mode="walking") #should return dataframe with commute times added


    
    assert 'Commute_Time' in result_df.columns #checking if new column added with specified mode
    assert len(result_df) == len(df) #checking if lengths match
    
    for commute_time in result_df['Commute_Time']: 
        assert isinstance(commute_time, (str, type(None))) #each index should be string or None
