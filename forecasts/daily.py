# Daily forecast logic

# forecasts/weekly.py
"""
Module for retrieving and displaying 1-day weather forecasts.
TODAY'S FORECAST: Thursday, March 20
----------------------------------------
🌡️ Temperature: High 42°F (3pm) | Low 32°F (8am)
   Feels like: 38°F - 28°F due to wind

☂️ Precipitation: Light snow in early morning (until 7am)
   Chance of precipitation: 80% morning, 10% afternoon

💨 Wind: Northwest 8-12 mph, gusting to 15 mph afternoon

⏰ TODAY AT A GLANCE:
   Morning (6am-12pm): Cold start with light snow clearing by 8am
   Afternoon (12pm-6pm): Sunny and clear, warming up
   Evening (6pm-10pm): Clear and cooling down

🚶 OUTDOOR ACTIVITY RATING: Good (7/10) - Best from 2pm-5pm

👔 WHAT TO WEAR: Winter coat in morning, light jacket sufficient by afternoon
"""

from datetime import datetime
from utils.config import WEATHER_CODES, DAYS
from utils.weather_api import get_daily_forecast
from utils.display import fahrenheit_from_celsius, get_avg_temp, get_opinion

def display_day_forecast(location_data):
    """Display a 7-day forecast for the given location."""
    print("Today's forecast:")
    
    forecast_data = get_daily_forecast(location_data, days=1)
    
    if not forecast_data:
        return
    
    try:
        times = forecast_data['daily']['time']
        weather_codes = forecast_data['daily']['weather_code']
        max_temps = forecast_data['daily']['temperature_2m_max']
        min_temps = forecast_data['daily']['temperature_2m_min']
        precipitation = forecast_data['daily']['precipitation_sum']
        
        for i in range(len(times)):
            date_obj = datetime.fromisoformat(times[i])
            month = date_obj.month
            weekday_name = DAYS[date_obj.weekday()]
            day_of_month = date_obj.day
            
            weather_code = weather_codes[i]
            weather_desc = WEATHER_CODES[weather_code]
            max_temp_f = fahrenheit_from_celsius(max_temps[i])
            min_temp_f = fahrenheit_from_celsius(min_temps[i])
            
            print(f"\nTODAY'S FORECAST: {weekday_name}, {month}/{day_of_month}:")
            print(f"🌡️ Temperature: High {max_temp_f}°F | Low {min_temp_f}°F")
            print(f"☂️ Precipitation: {precipitation} mm")
            print(f"Conditions: {weather_desc}")            
            print(f"Precipitation: {precipitation[i]} mm")
        
    except KeyError as e:
        print(f"Error processing forecast data: {e}")