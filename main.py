#!/usr/bin/env python3
"""
Main entry point for the weather application.
Provides debugging output to test current functionality.
"""

import os
import sys
import csv
import datetime
from typing import Dict, List, Optional

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Now import our modules
from models.Location import Location
from models.WeatherAPI import WeatherAPI
from models.WeatherCondition import WeatherCondition
from models.Forecast import Forecast

# Import config
from utils.config import ZIPCODE, WEATHER_CODES, DAYS

def load_zipcode_database(file_path: str = "utils/zipcodes.csv") -> List[Dict]:
    """Load zipcode database from CSV file."""
    zipcodes = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                zipcodes.append(row)
        print(f"Loaded {len(zipcodes)} zipcodes from {file_path}")
        return zipcodes
    except Exception as e:
        print(f"Error loading zipcode database: {e}")
        return []


def get_location_input() -> str:
    """Get zipcode input from user or use default."""
    try:
        return input("Enter zipcode (or press Enter for default): ") or ZIPCODE
    except:
        return ZIPCODE


def get_coords_from_zip(zipcode: str, zipcode_db: List[Dict]) -> Dict:
    """Find location data for a given zipcode."""
    for entry in zipcode_db:
        if entry.get('zip') == zipcode:
            # Create formatted display name
            display_name = f"{entry.get('city', '')}, {entry.get('state_id', '')}"
            
            # Return location data dictionary
            return {
                'lat': float(entry.get('lat', 0)),
                'lng': float(entry.get('lng', 0)),
                'city': entry.get('city', ''),
                'state': entry.get('state_id', ''),
                'display_name': display_name,
                'timezone': entry.get('timezone', 'America/Chicago')
            }
    
    # If zipcode not found, use default coordinates (central US)
    print(f"Zipcode {zipcode} not found. Using default location.")
    return {
        'lat': 40.0,
        'lng': -89.0,
        'city': 'Unknown',
        'state': 'IL',
        'display_name': 'Unknown Location',
        'timezone': 'America/Chicago'
    }


def create_weather_condition(time_str, temp, code, humidity=None, wind_speed=None, 
                            sunrise=None, sunset=None):
    """Create a WeatherCondition object from API data."""
    try:
        time_obj = datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        description = WEATHER_CODES.get(code, "Unknown")
        return WeatherCondition(
            time=time_obj,
            temperature=temp,
            weather_code=code,
            description=description,
            humidity=humidity,
            wind_speed=wind_speed,
            sunrise=sunrise,
            sunset=sunset
        )
    except Exception as e:
        print(f"Error creating weather condition: {e}")
        return None


def create_forecast_from_api_response(response, location):
    """Create a Forecast object from API response data."""
    if not response:
        print("Error: No API response data")
        return None
    
    try:
        # Extract start and end dates
        hourly_times = response.get('hourly', {}).get('time', [])
        start_date = datetime.datetime.fromisoformat(hourly_times[0].replace('Z', '+00:00')) if hourly_times else datetime.datetime.now()
        end_date = datetime.datetime.fromisoformat(hourly_times[-1].replace('Z', '+00:00')) if hourly_times else (datetime.datetime.now() + datetime.timedelta(days=7))
        
        # Create hourly conditions
        hourly_conditions = []
        hourly_data = response.get('hourly', {})
        hourly_times = hourly_data.get('time', [])
        hourly_temps = hourly_data.get('temperature_2m', [])
        hourly_codes = hourly_data.get('weather_code', [])
        hourly_humidity = hourly_data.get('relative_humidity_2m', [])
        hourly_wind = hourly_data.get('wind_speed_10m', [])
        hourly_precipitation = hourly_data.get('precipitation', [])
        
        # Daily data for sunrise/sunset
        daily_data = response.get('daily', {})
        daily_times = daily_data.get('time', [])
        sunrise_times = daily_data.get('sunrise', [])
        sunset_times = daily_data.get('sunset', [])
        
        # Create sunrise/sunset lookup by date
        sun_times = {}
        for i, day in enumerate(daily_times):
            if i < len(sunrise_times) and i < len(sunset_times):
                sun_times[day] = {
                    'sunrise': sunrise_times[i],
                    'sunset': sunset_times[i]
                }
        
        # Create hourly conditions
        for i in range(len(hourly_times)):
            if i < len(hourly_temps) and i < len(hourly_codes):
                # Get date part of timestamp for sunrise/sunset lookup
                date_part = hourly_times[i].split('T')[0]
                sunrise = sun_times.get(date_part, {}).get('sunrise')
                sunset = sun_times.get(date_part, {}).get('sunset')
                
                humidity = hourly_humidity[i] if i < len(hourly_humidity) else None
                wind = hourly_wind[i] if i < len(hourly_wind) else None
                
                # Add precipitation to condition if available
                condition = create_weather_condition(
                    hourly_times[i], hourly_temps[i], hourly_codes[i],
                    humidity, wind, sunrise, sunset
                )
                
                if condition and i < len(hourly_precipitation):
                    condition.precipitation = hourly_precipitation[i]
                
                hourly_conditions.append(condition)
        
        # Create daily conditions
        daily_conditions = []
        daily_high_temps = daily_data.get('temperature_2m_max', [])
        daily_low_temps = daily_data.get('temperature_2m_min', [])
        daily_codes = daily_data.get('weather_code', [])
        daily_precip = daily_data.get('precipitation_sum', [])
        daily_wind = daily_data.get('wind_speed_10m_max', [])
        
        for i in range(len(daily_times)):
            if i < len(daily_high_temps) and i < len(daily_low_temps) and i < len(daily_codes):
                # Get sunrise/sunset for this day
                sunrise = sun_times.get(daily_times[i], {}).get('sunrise')
                sunset = sun_times.get(daily_times[i], {}).get('sunset')
                
                # Create a time object for the day
                day_time = datetime.datetime.fromisoformat(daily_times[i])
                
                # Create a daily condition with the day's summary
                daily_condition = create_weather_condition(
                    daily_times[i], daily_high_temps[i], daily_codes[i],
                    None, daily_wind[i] if i < len(daily_wind) else None,
                    sunrise, sunset
                )
                
                # Add additional properties
                if daily_condition:
                    daily_condition.low_temp = daily_low_temps[i]
                    if i < len(daily_precip):
                        daily_condition.precipitation_sum = daily_precip[i]
                    
                    daily_conditions.append(daily_condition)
        
        # Create and return the forecast
        return Forecast(location, start_date, end_date, hourly_conditions, daily_conditions)
    
    except Exception as e:
        print(f"Error creating forecast: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main entry point for the weather application."""
    print("=== Weather App Debug Mode ===")
    
    # Load zipcode database
    print("Loading zipcode database...")
    zipcode_db = load_zipcode_database()
    
    # Get location from zipcode
    zipcode = get_location_input()
    print(f"Getting location data for zipcode: {zipcode}")
    location_data = get_coords_from_zip(zipcode, zipcode_db)
    
    # Create Location object
    location = Location.from_zipcode_data(location_data)
    print(f"Location: {location}")
    
    # Initialize the API client
    print("\nInitializing Weather API client...")
    weather_api = WeatherAPI()
    
    # Get weather data from API
    print(f"Requesting weather data for {location.city}, {location.state}...")
    
    # Configure what data to request
    hourly_vars = ["temperature_2m", "relative_humidity_2m", "precipitation", 
                   "weather_code", "wind_speed_10m"]
    daily_vars = ["temperature_2m_max", "temperature_2m_min", "weather_code",
                 "precipitation_sum", "precipitation_hours", "sunrise", "sunset", 
                 "wind_speed_10m_max"]
    
    try:
        api_response = weather_api.get_forecast(
            latitude=location.lat,
            longitude=location.lng,
            timezone=location.timezone,
            hourly=hourly_vars,
            daily=daily_vars,
            temperature_unit="fahrenheit"
        )
        
        if not api_response:
            print("Error: No response from weather API")
            sys.exit(1)
            
        # Print response structure for debugging
        print("\nAPI Response Structure:")
        for key in api_response.keys():
            if key in ['hourly', 'daily']:
                print(f"  {key}: {list(api_response[key].keys())}")
            else:
                print(f"  {key}: {type(api_response[key])}")
        
        # Create a Forecast object from the API response
        print("\nCreating Forecast object...")
        forecast = create_forecast_from_api_response(api_response, location)
        
        if forecast:
            # Get today's forecast with all relevant details
            today_forecast = forecast.getDayForecast()
            
            if today_forecast:
                print("\n===== TODAY'S FORECAST SUMMARY =====")
                print(f"Weather for {today_forecast['location']} on {today_forecast['date'].strftime('%A, %B %d')}:")
                print(f"{today_forecast['emoji']} {today_forecast['description']}")
                
                if today_forecast['high']['temp'] is not None:
                    high_time = today_forecast['high']['time'].strftime('%I:%M %p') if today_forecast['high']['time'] else "N/A"
                    print(f"High: {today_forecast['high']['temp']}°F at {high_time}")
                
                if today_forecast['low']['temp'] is not None:
                    low_time = today_forecast['low']['time'].strftime('%I:%M %p') if today_forecast['low']['time'] else "N/A"
                    print(f"Low: {today_forecast['low']['temp']}°F at {low_time}")
                
                print(f"Precipitation expected for {today_forecast['precipitation_hours']} hours")
            else:
                print("\nNo forecast data available for today")
        else:
            print("Failed to create forecast from API response")
    
    except Exception as e:
        print(f"Error in main function: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()