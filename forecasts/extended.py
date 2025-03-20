# 14-day forecast logic
# forecasts/weekly.py
"""
Module for retrieving and displaying 14-day weather forecasts.
"""

from datetime import datetime
from utils.config import WEATHER_CODES, DAYS
from utils.weather_api import get_forecast_data
from utils.display import fahrenheit_from_celsius, get_avg_temp, get_opinion

def display_extended_forecast(location_data):
    """Display a 14-day forecast for the given location."""
    print(f"14-day forecast:")
    
    # Get forecast data from API
    forecast_data = get_forecast_data(location_data, days = 14)
    
    if not forecast_data:
        return
    
    try:
        temp_list = forecast_data['hourly']['temperature_2m']
        cond_list = forecast_data['hourly']['weather_code']
        api_times = forecast_data['hourly']['time']
        
        current_day = None
        times_list = []
        temperatures = []
        
        # Process and display forecast
        for i in range(len(api_times)):
            code = cond_list[i]
            temp = fahrenheit_from_celsius(temp_list[i])
            time_str = api_times[i]
            cond = WEATHER_CODES[code]
            
            dateTimeObj = datetime.fromisoformat(time_str)
            date_only = dateTimeObj.date()
            day_of_month = dateTimeObj.day
            weekday_number = date_only.weekday()
            weekday_name = DAYS[weekday_number]
            time_display = dateTimeObj.strftime("%I:%M %p")
            
            formatted_label = f"{weekday_name} {time_display}"
            times_list.append(formatted_label)
            temperatures.append(temp)
            
            
            if current_day != date_only:
                current_day = date_only
                print(f"\n{weekday_name} the {day_of_month}th:")
            
            print(f"{time_display} {cond} {temp:.1f}°F")
        
        # Display opinion about average temperature
        avgTemp = get_avg_temp(temp_list)
        print(get_opinion(avgTemp))
        
    except KeyError as e:
        print(f"Error processing forecast data: {e}")