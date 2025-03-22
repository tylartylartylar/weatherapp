# models/weather_api/__init__.py
import requests
import json
from .constants import *
from .request import build_forecast_request
from .response import process_forecast_response

class WeatherAPI:
    """
    A comprehensive client for the Open-Meteo weather API.
    Supports all available parameters and forecast types.
    """
    
    # Base API URL
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self):
        """Initialize the Weather API client."""
        pass
    
    def get_forecast(self, latitude, longitude, **kwargs):
        """Get weather forecast with all specified parameters."""
        # Build parameters
        params = build_forecast_request(latitude, longitude, **kwargs)
        
        # Make API request
        return self._make_request(params)
    
    # [Your convenience methods would remain here]
    # get_current_weather, get_hourly_forecast, etc.
    
    def _make_request(self, params):
        """Execute an API request with the given parameters."""
        """
        Execute an API request with the given parameters.
        
        Args:
            params: Dictionary of request parameters
            
        Returns:
            dict: Parsed JSON response or None if request failed
        """
        try:
            response = requests.get(self.BASE_URL, params=params)
            
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                print(f"Request failed with status code: {response.status_code}")
                if response.text:
                    print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"Error making API request: {e}")
            return None