# forecasts/weekly.py
"""
Module for retrieving and displaying 7-day weather forecasts.
"""

from datetime import datetime
from utils.config import WEATHER_CODES, DAYS
from utils.weather_api import get_forecast_data
from utils.display import fahrenheit_from_celsius, get_avg_temp, get_opinion

def get_day_condition_summary(day_conditions):
    """
    Generate a summary of the day's weather conditions.
    
    Args:
        day_conditions: List of weather condition strings for a single day
    
    Returns:
        String summary like "Mostly sunny with evening clouds"
    """
    # Count occurrences of each condition
    condition_counts = {}
    for condition in day_conditions:
        condition_counts[condition] = condition_counts.get(condition, 0) + 1
    
    # Find the dominant condition
    dominant_condition = max(condition_counts, key=condition_counts.get)
    dominant_count = condition_counts[dominant_condition]
    
    # Check if it dominates the whole day
    if dominant_count >= len(day_conditions) * 0.75:
        return f"Consistently {dominant_condition.lower()}"
    
    # Check for morning/afternoon/evening patterns
    morning_conditions = day_conditions[0:6]  # 12am-6am
    daytime_conditions = day_conditions[6:18]  # 6am-6pm
    evening_conditions = day_conditions[18:]  # 6pm-12am
    
    # Find dominant conditions for each part of day
    morning_dominant = max(set(morning_conditions), key=morning_conditions.count)
    daytime_dominant = max(set(daytime_conditions), key=daytime_conditions.count)
    evening_dominant = max(set(evening_conditions), key=evening_conditions.count)
    
    # Create a summary based on time of day patterns
    if morning_dominant == daytime_dominant == evening_dominant:
        return f"Consistently {morning_dominant.lower()}"
    elif morning_dominant != daytime_dominant and daytime_dominant == evening_dominant:
        return f"{morning_dominant} morning, becoming {daytime_dominant.lower()}"
    elif morning_dominant == daytime_dominant and daytime_dominant != evening_dominant:
        return f"Mostly {morning_dominant.lower()} with {evening_dominant.lower()} evening"
    else:
        return f"{morning_dominant} morning, {daytime_dominant} afternoon, {evening_dominant} evening"

def display_weekly_forecast(location_data):
    """Display an enhanced 7-day forecast for the given location."""
    print(f"7-day forecast:")
    
    # Get forecast data from API
    forecast_data = get_forecast_data(location_data, days=7)
    
    if not forecast_data:
        return
    
    try:
        temp_list = forecast_data['hourly']['temperature_2m']
        cond_list = forecast_data['hourly']['weather_code']
        api_times = forecast_data['hourly']['time']
        
        # Group data by day
        days_data = {}  # Will store data by date
        
        for i in range(len(api_times)):
            code = cond_list[i]
            temp = fahrenheit_from_celsius(temp_list[i])
            time_str = api_times[i]
            condition = WEATHER_CODES[code]
            
            date_time_obj = datetime.fromisoformat(time_str)
            date_only = date_time_obj.date().isoformat()
            
            # Initialize day data if this is a new day
            if date_only not in days_data:
                days_data[date_only] = {
                    'temps': [],
                    'conditions': [],
                    'times': [],
                    'date_obj': date_time_obj.date()
                }
            
            # Add this hour's data to the day
            days_data[date_only]['temps'].append(temp)
            days_data[date_only]['conditions'].append(condition)
            days_data[date_only]['times'].append(date_time_obj)
        
        # Now process each day to show summary and details
        for date in sorted(days_data.keys()):
            day_data = days_data[date]
            date_obj = day_data['date_obj']
            weekday_name = DAYS[date_obj.weekday()]
            
            # Calculate day summary
            high_temp = max(day_data['temps'])
            low_temp = min(day_data['temps'])
            temp_range = high_temp - low_temp
            condition_summary = get_day_condition_summary(day_data['conditions'])
            
            # Display day header and summary
            print(f"\n{weekday_name}, {date_obj.month}/{date_obj.day}:")
            print(f"  Summary: High {high_temp:.1f}°F, Low {low_temp:.1f}°F")
            print(f"  Conditions: {condition_summary}")
            
            # Add weather tips based on conditions
            if any("rain" in c.lower() or "drizzle" in c.lower() for c in day_data['conditions']):
                print("  Tip: Don't forget your umbrella!")
            elif any("snow" in c.lower() for c in day_data['conditions']):
                print("  Tip: Plan for slower travel and dress warmly")
            elif high_temp > 80:
                print("  Tip: Stay hydrated and consider sun protection")
            elif temp_range > 20:
                print(f"  Tip: Dress in layers (temperature swing of {temp_range:.1f}°F)")
            
            print("\n  Hourly Forecast:")
            
            # Display hourly data
            for i in range(len(day_data['times'])):
                time_display = day_data['times'][i].strftime("%I:%M %p")
                print(f"  {time_display} {day_data['conditions'][i]} {day_data['temps'][i]:.1f}°F")
        
        # Display opinion about average temperature
        avg_temp = get_avg_temp(temp_list)
        print(f"\nWeekly average: {fahrenheit_from_celsius(avg_temp):.1f}°F")
        print(get_opinion(avg_temp))
        
    except KeyError as e:
        print(f"Error processing forecast data: {e}")