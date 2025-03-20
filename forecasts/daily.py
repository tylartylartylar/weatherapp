# Daily forecast logic

# forecasts/weekly.py
"""
Module for retrieving and displaying 1-day weather forecasts.
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
            
            print(f"\n{weekday_name}, {month}/{day_of_month}:")
            print(f"Conditions: {weather_desc}")
            print(f"Low of {min_temp_f:.1f}°F, High of {max_temp_f:.1f}°F")
            print(f"Precipitation: {precipitation[i]} mm")
        
    except KeyError as e:
        print(f"Error processing forecast data: {e}")