"""Functions for building API requests to Open-Meteo."""
'''
builds all the request parameters needed to make a successful call to the Open-Meteo weather API.
'''

from typing import Dict, List, Union, Optional
from .constants import UNITS, CELL_SELECTIONS, PRESSURE_LEVELS, WEATHER_MODELS

def build_forecast_request(
                         latitude: Union[float, List[float]], 
                         longitude: Union[float, List[float]],
                         elevation: Optional[Union[float, List[float]]] = None,
                         hourly: Optional[List[str]] = None,
                         daily: Optional[List[str]] = None,
                         current: Optional[List[str]] = None,
                         minutely_15: Optional[List[str]] = None,
                         temperature_unit: str = "celsius",
                         wind_speed_unit: str = "kmh",
                         precipitation_unit: str = "mm",
                         timeformat: str = "iso8601",
                         timezone: Union[str, List[str]] = "GMT",
                         past_days: int = 0,
                         forecast_days: int = 7,
                         forecast_hours: Optional[int] = None,
                         forecast_minutely_15: Optional[int] = None,
                         past_hours: Optional[int] = None,
                         past_minutely_15: Optional[int] = None,
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None,
                         start_hour: Optional[str] = None,
                         end_hour: Optional[str] = None,
                         start_minutely_15: Optional[str] = None,
                         end_minutely_15: Optional[str] = None,
                         models: Optional[List[str]] = None,
                         cell_selection: str = "land",
                         apikey: Optional[str] = None,
                         pressure_level: Optional[List[int]] = None,
                         tilt: Optional[float] = None,
                         azimuth: Optional[float] = None) -> Dict:
    
    params = {}
    
    if isinstance(latitude, list) and isinstance(longitude, list):
        if len(latitude) != len(longitude):
            raise ValueError("Latitude and longitude lists must have the same length")
        params["latitude"] = ",".join(str(lat) for lat in latitude)
        params["longitude"] = ",".join(str(lon) for lon in longitude)
    else:
        params["latitude"] = latitude
        params["longitude"] = longitude
    
    if elevation is not None:
        if isinstance(elevation, list):
            params["elevation"] = ",".join(str(elev) for elev in elevation)
        else:
            params["elevation"] = elevation
    
    if hourly:
        params["hourly"] = ",".join(hourly)
        
    if daily:
        params["daily"] = ",".join(daily)
        
    if current:
        params["current"] = ",".join(current)
        
    if minutely_15:
        params["minutely_15"] = ",".join(minutely_15)
    
    if temperature_unit and temperature_unit in UNITS["temperature"]:
        params["temperature_unit"] = temperature_unit
        
    if wind_speed_unit and wind_speed_unit in UNITS["wind_speed"]:
        params["wind_speed_unit"] = wind_speed_unit
        
    if precipitation_unit and precipitation_unit in UNITS["precipitation"]:
        params["precipitation_unit"] = precipitation_unit
        
    if timeformat and timeformat in UNITS["timeformat"]:
        params["timeformat"] = timeformat
    
    if timezone:
        if isinstance(timezone, list):
            params["timezone"] = ",".join(timezone)
        else:
            params["timezone"] = timezone
    
    if past_days is not None:
        params["past_days"] = past_days
        
    if forecast_days is not None:
        params["forecast_days"] = forecast_days
        
    if forecast_hours is not None:
        params["forecast_hours"] = forecast_hours
        
    if forecast_minutely_15 is not None:
        params["forecast_minutely_15"] = forecast_minutely_15
        
    if past_hours is not None:
        params["past_hours"] = past_hours
        
    if past_minutely_15 is not None:
        params["past_minutely_15"] = past_minutely_15
    
    if start_date:
        params["start_date"] = start_date
        
    if end_date:
        params["end_date"] = end_date
        
    if start_hour:
        params["start_hour"] = start_hour
        
    if end_hour:
        params["end_hour"] = end_hour
        
    if start_minutely_15:
        params["start_minutely_15"] = start_minutely_15
        
    if end_minutely_15:
        params["end_minutely_15"] = end_minutely_15
    
    if models:
        params["models"] = ",".join(models)
    
    if cell_selection in CELL_SELECTIONS:
        params["cell_selection"] = cell_selection
    
    if apikey:
        params["apikey"] = apikey
    
    if pressure_level:
        valid_levels = [level for level in pressure_level if level in PRESSURE_LEVELS]
        if valid_levels:
            params["pressure_level"] = ",".join(str(level) for level in valid_levels)
    
    if tilt is not None:
        params["tilt"] = tilt
        
    if azimuth is not None:
        params["azimuth"] = azimuth
    
    return params