import requests
import json
from typing import Dict, List, Union, Optional, Any
from constants import BASE_URL
from request import build_forecast_request
from response import process_forecast_response

class WeatherAPI:
    def get_forecast(self, latitude, longitude, **kwargs):
        params = build_forecast_request(latitude, longitude, **kwargs)
        response = self._make_request(params)
        return process_forecast_response(response)
    
    def _make_request(self, params):
        try:
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                try:
                    data = json.loads(response.text)
                    
                    if not data:
                        print("Empty response from API")
                        return None

                    return data
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON response: {e}")
                    print(f"Response text: {response.text[:100]}...")
                    return None
                
            else:
                print(f"Request failed with status code: {response.status_code}")
                if response.text:
                    print(f"Response: {response.text}")
                return None
            
        except requests.RequestException as e:
            print(f"Error making API request: {e}")
            return None
        