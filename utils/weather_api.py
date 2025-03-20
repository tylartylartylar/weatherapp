"""
Module for interacting with the Open-Meteo weather API.
"""

import requests
import json

# Base API configuration
API_BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Default parameter configurations for different forecast types
FORECAST_PARAMS = {
    "hourly": {
        "weather_code": True,
        "temperature_2m": True,
        "precipitation_probability": True,
        "windspeed_10m": True
    },
    "daily": {
        "weather_code": True,
        "temperature_2m_max": True,
        "temperature_2m_min": True,
        "precipitation_sum": True
    },
    "current": {
        "temperature_2m": True,
        "weather_code": True, 
        "wind_speed_10m": True
    }
}

def build_api_params(location_data, days=7, forecast_types=None, custom_params=None):
    """
    Build parameters for the Open-Meteo API request.
    
    Args:
        location_data (dict): Dictionary containing lat, lng, and timezone
        days (int): Number of forecast days to retrieve
        forecast_types (list): List of forecast types to request (e.g., ['hourly', 'daily'])
        custom_params (dict): Custom parameters for each forecast type
            e.g., {'hourly': ['temperature_2m', 'weather_code']}
    
    Returns:
        dict: Parameters for the API request
    """
    # Base parameters required for all requests
    params = {
        "latitude": location_data['lat'],
        "longitude": location_data['lng'],
        "timezone": location_data['timezone'],
        "forecast_days": days
    }
    
    # If no forecast types specified, default to hourly
    if not forecast_types:
        forecast_types = ["hourly"]
    
    # Add parameters for each forecast type
    for forecast_type in forecast_types:
        if forecast_type in FORECAST_PARAMS:
            # Use custom parameters if provided, otherwise use defaults
            if custom_params and forecast_type in custom_params:
                params[forecast_type] = ",".join(custom_params[forecast_type])
            else:
                # Get default parameters for this forecast type
                default_params = [param for param, include in FORECAST_PARAMS[forecast_type].items() if include]
                params[forecast_type] = ",".join(default_params)
    
    return params

def make_api_request(params):
    """
    Make a request to the Open-Meteo API.
    
    Args:
        params (dict): Parameters for the API request
    
    Returns:
        dict: API response data if successful, None otherwise
    """
    try:
        response = requests.get(API_BASE_URL, params=params)
        
        # For debugging
        # print(f"Request URL: {response.url}")
        
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"Request failed with status code: {response.status_code}")
            # For debugging
            # print(f"Response content: {response.text}")
            return None
    except Exception as e:
        print(f"Error making API request: {e}")
        return None

def get_forecast_data(location_data, days=7, forecast_types=None, custom_params=None):
    """
    Get weather forecast data from Open-Meteo API.
    
    Args:
        location_data (dict): Dictionary containing lat, lng, and timezone
        days (int): Number of forecast days to retrieve (default: 7)
        forecast_types (list): Types of forecast to retrieve (e.g., ['hourly', 'daily'])
        custom_params (dict): Custom parameters for each forecast type
    
    Returns:
        dict: API response data if successful, None otherwise
    """
    # For backward compatibility
    if isinstance(forecast_types, str):
        forecast_types = [forecast_types]
    
    # Build API parameters
    params = build_api_params(location_data, days, forecast_types, custom_params)
    
    # Make API request
    return make_api_request(params)

# Helper functions for common forecast types
def get_hourly_forecast(location_data, days=7):
    """Get hourly forecast for the specified location."""
    return get_forecast_data(location_data, days, ["hourly"])

def get_daily_forecast(location_data, days=7):
    """Get daily forecast for the specified location."""
    return get_forecast_data(location_data, days, ["daily"])

def get_current_weather(location_data):
    """Get current weather for the specified location."""
    return get_forecast_data(location_data, 1, ["current"])

def get_complete_forecast(location_data, days=7):
    """Get complete forecast including hourly and daily data."""
    return get_forecast_data(location_data, days, ["hourly", "daily"])