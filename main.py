import csv
import requests
import json
from datetime import datetime, timedelta

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
            'timezone': data['timezone']
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
    
    zipcode_db = load_zipcode_database()
    
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
        }
    
    zipcode = getLocationInput()
    
    if zipcode and zipcode_db:
        print(f"Trying to find coordinates for {zipcode}...\n")
        location_data = get_coords_from_zip(zipcode, zipcode_db)
        if location_data:
            print(f"Location: {location_data['display_name']}")
            print(f"Coordinates: {location_data['lat']}, {location_data['lng']}")
            
            print(f"7-day forecast:")
            
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
            "latitude": location_data['lat'],
            "longitude": location_data['lng'],
            "timezone": location_data['timezone'],
            "forecast_days": 7,
            "hourly": "weather_code,temperature_2m,precipitation_probability,windspeed_10m"
}
            
            response = requests.get(url, params=params)
            body = response.text
            body_dict = json.loads(body)
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            if response.status_code == 200:
                try:
                    temp_list = body_dict['hourly']['temperature_2m']
                    cond_list = body_dict['hourly']['weather_code']
                    times = body_dict['hourly']['time']

                    # Group forecasts by day
                    current_day = None
                    
                    for i in range(len(times)):
                        code = cond_list[i]
                        temp = (temp_list[i] * 9/5) + 32
                        time_str = times[i]
                        cond = weather_codes[code]
                        
                        dateTimeObj = datetime.fromisoformat(time_str)
                        date_only = dateTimeObj.date()
                        day_of_month = dateTimeObj.day
                        weekday_number = date_only.weekday()
                        weekday_name = days[weekday_number]
                        time_display = dateTimeObj.strftime("%I:%M %p")
                        
                        # Print the day header when we reach a new day
                        if current_day != date_only:
                            current_day = date_only
                            print(f"\n{weekday_name} the {day_of_month}th:")
                        
                        # Print the forecast line
                        print(f"{time_display} {cond} {temp:.1f}°F")
                    
                except ValueError:
                    print("response is not valid JSON")
            else:
                print(f"Request failed with status code: {response.status_code}")
            
        else:
            print("Could not find coordinates for this zipcode.")
    else:
        print("Exiting program.")
    
if __name__ =="__main__":
    main()