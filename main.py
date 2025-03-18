import csv
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

def load_zipcode_database(filename="zipcodes.csv"):
    zipcode_dict = {}
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                zipcode = str(row['zip']).zfill(5)
                zipcode_dict[zipcode] = {
                    'lat': float(row['lat']),
                    'lng': float(row['lng']),
                    'city': row['city'],
                    'state_id': row['state_id'],
                    'state_name': row['state_name'],
                    'timezone': row['timezone']
                }
        print(f"Loaded {len(zipcode_dict)} zipcodes from database.")
        return zipcode_dict
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
        return {}
    except Exception as e:
        print(f"Error loading zipcode database: {e}")
        return {}
    
def get_coords_from_zip(zipcode, zipcode_db):
    if zipcode in zipcode_db:
        data = zipcode_db[zipcode]
        return {
            'lat': data['lat'],
            'lng': data['lng'],
            'display_name': f"{data['city']}, {data['state_id']}",
            'timezone': data['timezone']  # Added timezone here
        }
    
    print(f"Zipcode {zipcode} not found in database.")
    return None    

def getLocationInput():
    user_location = input("Please enter your current 5-digit Zipcode XXXXX\n-> ")
    if len(user_location) == 5 and user_location.isdigit():
        return user_location
    else:
        print(f"Supplied zipcode invalid length... {user_location}")
        retry = input("would you like to retry? (Y/n)")
        if retry.lower() == "y":
            return getLocationInput()
        else:
            print(f"Supplied zipcode invalid length... Maybe go outside to check the weather until I can implement search by city/state")
            return None

def main():
    # Setup the Open-Meteo API client
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    
    zipcode_db = load_zipcode_database()
    
    zipcode = getLocationInput()
    
    if zipcode and zipcode_db:
        print(f"Trying to find coordinates for {zipcode}...\n")
        location_data = get_coords_from_zip(zipcode, zipcode_db)
        if location_data:
            print(f"Location: {location_data['display_name']}")
            print(f"Coordinates: {location_data['lat']}, {location_data['lng']}")
            
            print(f"Getting basic forecast for {location_data['display_name']}...")
            
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": location_data['lat'],
                "longitude": location_data['lng'],
                "timezone": location_data['timezone'],
                "forecast_days": 7,
                "hourly": "weather_code"  # Added hourly parameter
            }
            
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]
            print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
            print(f"Elevation {response.Elevation()} m asl")
            print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
            print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
            hourly = response.Hourly()
            hourly_weather_code = hourly.Variables(0).ValuesAsNumpy()

            hourly_data = {"date": pd.date_range(
                start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
                end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = hourly.Interval()),
                inclusive = "left"
            )}
            
            hourly_data["weather_code"] = hourly_weather_code  # Fixed indentation

            hourly_dataframe = pd.DataFrame(data = hourly_data)
            print(hourly_dataframe)
        else:
            print("Could not find coordinates for this zipcode.")
    else:
        print("Exiting program.")
    
if __name__ =="__main__":
    main()