"""Functions for processing API responses from Open-Meteo."""

from typing import Dict, Optional, Any

def process_forecast_response(response: Dict) -> Dict:
    if not response:
        return None
        
    if 'error' in response:
        print(f"API returned an error: {response.get('reason', 'Unknown error')}")
        return None
    
    required_sections = ['latitude', 'longitude', 'timezone']
    for section in required_sections:
        if section not in response:
            print(f"Warning: Response missing '{section}' section")
    
    return response
    
def extract_weather_data(response: Dict, data_type: str) -> Dict:
    
    if not response or data_type not in response:
        return {}
        
    return response[data_type]