from models import Location
from models.weatherapi.WeatherAPI import WeatherAPI
from utils.get_location import load_zipcode_database, getLocationInput

def main():
    zipcode_db = load_zipcode_database()
    zipcode = getLocationInput()
    
    for entry in zipcode_db:
        if entry.get('zip') == zipcode:
            location_data = {
                'lat': float(entry.get('lat', 0)),
                'lng': float(entry.get('lng', 0)),
                'city': entry.get('city', ''),
                'state': entry.get('state_id', ''),
                'display_name': f"{entry.get('city', '')}, {entry.get('state_id', '')}",
                'timezone': entry.get('timezone', 'America/Chicago')
            }
            location = Location.from_zipcode_data(location_data)
            break
    else:
        print(f"Zipcode {zipcode} not found. Using default location.")
        
    weather_api = WeatherAPI()
    
    forecast_data = weather_api.get_forecast(        
        latitude=location.lat,
        longitude=location.lng,
        hourly=["temperature_2m", "weather_code"],
        daily=["temperature_2m_max", "temperature_2m_min", "weather_code"],
        timezone=location.timezone,
        temperature_unit="fahrenheit"
    )
    if forecast_data:
        print(f"Weather forecast for {location.display_name}")

    else:
        print("Unable to retrieve forecast data.")    
    

if __name__ == "__main__":
    main()