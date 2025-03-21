"""
Comprehensive module for interacting with the Open-Meteo weather API.
Supports all available parameters and forecast types.
"""

import requests
import json
from typing import Dict, List, Union, Optional, Any

class WeatherAPI:
    """
    A modular class for interacting with the Open-Meteo weather API.
    Supports all available parameters and forecast types.
    """
    
    # Base API URL
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    # Standard units
    UNITS = {
        "temperature": ["celsius", "fahrenheit"],
        "wind_speed": ["kmh", "ms", "mph", "kn"],
        "precipitation": ["mm", "inch"],
        "timeformat": ["iso8601", "unixtime"]
    }
    
    # All available hourly variables
    HOURLY_VARIABLES = [
        # Temperature and Humidity
        "temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature",
        
        # Pressure
        "pressure_msl", "surface_pressure",
        
        # Clouds
        "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high",
        
        # Wind
        "wind_speed_10m", "wind_speed_80m", "wind_speed_120m", "wind_speed_180m",
        "wind_direction_10m", "wind_direction_80m", "wind_direction_120m", "wind_direction_180m",
        "wind_gusts_10m",
        
        # Solar Radiation
        "shortwave_radiation", "direct_radiation", "direct_normal_irradiance", 
        "diffuse_radiation", "global_tilted_irradiance",
        
        # Other atmospheric
        "vapour_pressure_deficit", "cape", "evapotranspiration", "et0_fao_evapotranspiration",
        
        # Precipitation
        "precipitation", "snowfall", "precipitation_probability", "rain", "showers",
        
        # Conditions
        "weather_code", "snow_depth", "freezing_level_height", "visibility", "is_day",
        
        # Soil
        "soil_temperature_0cm", "soil_temperature_6cm", "soil_temperature_18cm", "soil_temperature_54cm",
        "soil_moisture_0_to_1cm", "soil_moisture_1_to_3cm", "soil_moisture_3_to_9cm", 
        "soil_moisture_9_to_27cm", "soil_moisture_27_to_81cm"
    ]
    
    # All available daily variables
    DAILY_VARIABLES = [
        "weather_code", 
        "temperature_2m_max", "temperature_2m_min",
        "apparent_temperature_max", "apparent_temperature_min",
        "sunrise", "sunset", "daylight_duration", "sunshine_duration",
        "uv_index_max", "uv_index_clear_sky_max",
        "precipitation_sum", "rain_sum", "showers_sum", "snowfall_sum",
        "precipitation_hours", "precipitation_probability_max", "precipitation_probability_min", 
        "precipitation_probability_mean",
        "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant",
        "shortwave_radiation_sum", "et0_fao_evapotranspiration"
    ]
    
    # All available current variables
    CURRENT_VARIABLES = [
        "temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day",
        "precipitation", "rain", "showers", "snowfall", "weather_code",
        "cloud_cover", "pressure_msl", "surface_pressure",
        "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"
    ]
    
    # All available 15-minutely variables
    MINUTELY_15_VARIABLES = [
        "temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature",
        "precipitation", "rain", "showers", "snowfall", "snowfall_height",
        "freezing_level_height", "cape", "wind_speed_10m", "wind_speed_80m",
        "wind_direction_10m", "wind_direction_80m", "wind_gusts_10m",
        "shortwave_radiation", "direct_radiation", "direct_normal_irradiance",
        "diffuse_radiation", "global_tilted_irradiance", "global_tilted_irradiance_instant",
        "sunshine_duration", "lightning_potential", "visibility", "weather_code"
    ]
    
    # Pressure level variables (for each pressure level)
    PRESSURE_LEVEL_VARIABLES = [
        "temperature", "relative_humidity", "dew_point", 
        "cloud_cover", "wind_speed", "wind_direction", "geopotential_height"
    ]
    
    # Available pressure levels in hPa
    PRESSURE_LEVELS = [
        1000, 975, 950, 925, 900, 850, 800, 700, 600, 500, 
        400, 300, 250, 200, 150, 100, 70, 50, 30
    ]
    
    # Weather models
    WEATHER_MODELS = [
        "best_match", "icon_seamless", "icon_global", "icon_eu", "icon_d2",
        "gfs_seamless", "gfs_global", "gfs_hrrr", "gfs_hrrr_alaska",
        "ecmwf_seamless", "ecmwf_ifs", "ecmwf_aifs",
        "metno_nordic", "harmonie_knmi", "gem_seamless", "gem_global", "gem_regional", "gem_hrdps",
        "meteofrance_seamless", "meteofrance_arpege", "meteofrance_arome",
        "jma_seamless", "jma_msm", "jma_gsm", "cma_grapes_global", "ukmo_global", "bom_access_global",
        "era5", "era5_land", "cerra", "cerra_land", "optionally_ensemble"
    ]
    
    # Cell selection options
    CELL_SELECTIONS = ["land", "sea", "nearest"]
    
    def __init__(self):
        """Initialize the Weather API client."""
        pass
    
    def build_forecast_request(self, 
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
                              # Additional parameters for pressure levels and solar radiation
                              pressure_level: Optional[List[int]] = None,
                              tilt: Optional[float] = None,
                              azimuth: Optional[float] = None) -> Dict:
        """
        Build a comprehensive request to the Open-Meteo API with all possible parameters.
        
        Args:
            latitude: Geographical WGS84 coordinate (single float or list for multiple locations)
            longitude: Geographical WGS84 coordinate (single float or list for multiple locations)
            elevation: The elevation used for downscaling (optional)
            hourly: List of hourly weather variables
            daily: List of daily weather variable aggregations
            current: List of current weather variables
            minutely_15: List of 15-minutely weather variables
            temperature_unit: Unit for temperature values (celsius, fahrenheit)
            wind_speed_unit: Unit for wind speed (kmh, ms, mph, kn)
            precipitation_unit: Unit for precipitation amounts (mm, inch)
            timeformat: Time format for timestamps (iso8601, unixtime)
            timezone: Timezone for timestamps (IANA time zone, e.g., "America/New_York")
            past_days: Number of days in the past (0-92)
            forecast_days: Number of days in the future (0-16)
            forecast_hours: Number of hours to forecast
            forecast_minutely_15: Number of 15-minute intervals to forecast
            past_hours: Number of past hours
            past_minutely_15: Number of past 15-minute intervals
            start_date: Start date for custom time interval (YYYY-MM-DD)
            end_date: End date for custom time interval (YYYY-MM-DD)
            start_hour: Start hour for custom hourly time interval (YYYY-MM-DDThh:mm)
            end_hour: End hour for custom hourly time interval (YYYY-MM-DDThh:mm)
            start_minutely_15: Start time for custom 15-minutely time interval (YYYY-MM-DDThh:mm)
            end_minutely_15: End time for custom 15-minutely time interval (YYYY-MM-DDThh:mm)
            models: List of weather models to use (defaults to auto-selection)
            cell_selection: Strategy for grid-cell selection (land, sea, nearest)
            apikey: API key for commercial usage
            pressure_level: List of pressure levels (hPa) for pressure level variables
            tilt: Panel tilt for global_tilted_irradiance (0-90)
            azimuth: Panel azimuth for global_tilted_irradiance (0 = south, -90 = east, 90 = west)
            
        Returns:
            dict: Parameters for the API request
        """
        # Build base parameters (required)
        params = {}
        
        # Handle single or multiple coordinates
        if isinstance(latitude, list) and isinstance(longitude, list):
            if len(latitude) != len(longitude):
                raise ValueError("Latitude and longitude lists must have the same length")
            params["latitude"] = ",".join(str(lat) for lat in latitude)
            params["longitude"] = ",".join(str(lon) for lon in longitude)
        else:
            params["latitude"] = latitude
            params["longitude"] = longitude
        
        # Optional elevation parameter
        if elevation is not None:
            if isinstance(elevation, list):
                params["elevation"] = ",".join(str(elev) for elev in elevation)
            else:
                params["elevation"] = elevation
        
        # Add forecast types if specified
        if hourly:
            params["hourly"] = ",".join(hourly)
            
        if daily:
            params["daily"] = ",".join(daily)
            
        if current:
            params["current"] = ",".join(current)
            
        if minutely_15:
            params["minutely_15"] = ",".join(minutely_15)
        
        # Units
        if temperature_unit and temperature_unit in self.UNITS["temperature"]:
            params["temperature_unit"] = temperature_unit
            
        if wind_speed_unit and wind_speed_unit in self.UNITS["wind_speed"]:
            params["wind_speed_unit"] = wind_speed_unit
            
        if precipitation_unit and precipitation_unit in self.UNITS["precipitation"]:
            params["precipitation_unit"] = precipitation_unit
            
        if timeformat and timeformat in self.UNITS["timeformat"]:
            params["timeformat"] = timeformat
        
        # Timezone
        if timezone:
            if isinstance(timezone, list):
                params["timezone"] = ",".join(timezone)
            else:
                params["timezone"] = timezone
        
        # Time range parameters
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
        
        # Custom date ranges
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
        
        # Weather models
        if models:
            params["models"] = ",".join(models)
        
        # Cell selection strategy
        if cell_selection in self.CELL_SELECTIONS:
            params["cell_selection"] = cell_selection
        
        # Commercial API key
        if apikey:
            params["apikey"] = apikey
        
        # Pressure level variables
        if pressure_level:
            # Ensure valid pressure levels
            valid_levels = [level for level in pressure_level if level in self.PRESSURE_LEVELS]
            if valid_levels:
                params["pressure_level"] = ",".join(str(level) for level in valid_levels)
        
        # Global tilted irradiance parameters
        if tilt is not None:
            params["tilt"] = tilt
            
        if azimuth is not None:
            params["azimuth"] = azimuth
        
        return params
    
    def make_request(self, params: Dict) -> Dict:
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
    
    def get_forecast(self, 
                   latitude: Union[float, List[float]], 
                   longitude: Union[float, List[float]],
                   **kwargs) -> Dict:
        """
        Get weather forecast with all specified parameters.
        
        Args:
            latitude: Geographical WGS84 coordinate
            longitude: Geographical WGS84 coordinate
            **kwargs: All other optional parameters supported by build_forecast_request
            
        Returns:
            dict: Weather forecast data
        """
        # Build parameters
        params = self.build_forecast_request(latitude, longitude, **kwargs)
        
        # Make API request
        return self.make_request(params)
    
    # Convenience methods for common forecast types
    def get_current_weather(self, 
                          latitude: Union[float, List[float]], 
                          longitude: Union[float, List[float]],
                          **kwargs) -> Dict:
        """
        Get current weather conditions.
        
        Args:
            latitude: Geographical WGS84 coordinate
            longitude: Geographical WGS84 coordinate
            **kwargs: Additional parameters
            
        Returns:
            dict: Current weather data
        """
        # Set default current weather variables if not specified
        if "current" not in kwargs or not kwargs["current"]:
            kwargs["current"] = self.CURRENT_VARIABLES
            
        return self.get_forecast(latitude, longitude, forecast_days=1, **kwargs)
    
    def get_hourly_forecast(self, 
                          latitude: Union[float, List[float]], 
                          longitude: Union[float, List[float]],
                          days: int = 7,
                          variables: Optional[List[str]] = None,
                          **kwargs) -> Dict:
        """
        Get hourly weather forecast.
        
        Args:
            latitude: Geographical WGS84 coordinate
            longitude: Geographical WGS84 coordinate
            days: Number of forecast days
            variables: List of hourly variables (defaults to common ones if not specified)
            **kwargs: Additional parameters
            
        Returns:
            dict: Hourly forecast data
        """
        if variables is None:
            # Default to some common variables
            variables = ["temperature_2m", "relative_humidity_2m", 
                         "precipitation_probability", "precipitation", 
                         "weather_code", "wind_speed_10m"]
            
        kwargs["hourly"] = variables
        kwargs["forecast_days"] = days
        
        return self.get_forecast(latitude, longitude, **kwargs)
    
    def get_daily_forecast(self, 
                         latitude: Union[float, List[float]], 
                         longitude: Union[float, List[float]],
                         days: int = 7,
                         variables: Optional[List[str]] = None,
                         **kwargs) -> Dict:
        """
        Get daily weather forecast.
        
        Args:
            latitude: Geographical WGS84 coordinate
            longitude: Geographical WGS84 coordinate
            days: Number of forecast days
            variables: List of daily variables (defaults to common ones if not specified)
            **kwargs: Additional parameters
            
        Returns:
            dict: Daily forecast data
        """
        if variables is None:
            # Default to some common variables
            variables = ["weather_code", "temperature_2m_max", "temperature_2m_min",
                         "precipitation_sum", "precipitation_probability_max",
                         "wind_speed_10m_max", "wind_gusts_10m_max"]
            
        kwargs["daily"] = variables
        kwargs["forecast_days"] = days
        
        return self.get_forecast(latitude, longitude, **kwargs)
    
    def get_minutely_forecast(self, 
                            latitude: Union[float, List[float]], 
                            longitude: Union[float, List[float]],
                            hours: int = 24,
                            variables: Optional[List[str]] = None,
                            **kwargs) -> Dict:
        """
        Get 15-minutely weather forecast.
        
        Args:
            latitude: Geographical WGS84 coordinate
            longitude: Geographical WGS84 coordinate
            hours: Number of forecast hours
            variables: List of 15-minutely variables
            **kwargs: Additional parameters
            
        Returns:
            dict: 15-minutely forecast data
        """
        if variables is None:
            # Default to some common variables
            variables = ["temperature_2m", "precipitation", "weather_code"]
            
        kwargs["minutely_15"] = variables
        kwargs["forecast_minutely_15"] = hours * 4  # Convert hours to 15-minute intervals
        
        return self.get_forecast(latitude, longitude, **kwargs)
    
    def get_complete_forecast(self, 
                            latitude: Union[float, List[float]], 
                            longitude: Union[float, List[float]],
                            days: int = 7,
                            hourly_variables: Optional[List[str]] = None,
                            daily_variables: Optional[List[str]] = None,
                            current_variables: Optional[List[str]] = None,
                            **kwargs) -> Dict:
        """
        Get complete forecast including hourly, daily and current data.
        
        Args:
            latitude: Geographical WGS84 coordinate
            longitude: Geographical WGS84 coordinate
            days: Number of forecast days
            hourly_variables: List of hourly variables
            daily_variables: List of daily variables
            current_variables: List of current variables
            **kwargs: Additional parameters
            
        Returns:
            dict: Complete forecast data
        """
        if hourly_variables is None:
            hourly_variables = ["temperature_2m", "relative_humidity_2m", 
                              "precipitation_probability", "precipitation", 
                              "weather_code", "wind_speed_10m"]
            
        if daily_variables is None:
            daily_variables = ["weather_code", "temperature_2m_max", "temperature_2m_min",
                             "precipitation_sum", "precipitation_probability_max"]
            
        if current_variables is None:
            current_variables = ["temperature_2m", "relative_humidity_2m", 
                               "weather_code", "wind_speed_10m"]
            
        kwargs["hourly"] = hourly_variables
        kwargs["daily"] = daily_variables
        kwargs["current"] = current_variables
        kwargs["forecast_days"] = days
        
        return self.get_forecast(latitude, longitude, **kwargs)
    
    # Static helper methods
    @staticmethod
    def get_all_hourly_variables() -> List[str]:
        """Get all available hourly variables."""
        return WeatherAPI.HOURLY_VARIABLES.copy()
    
    @staticmethod
    def get_all_daily_variables() -> List[str]:
        """Get all available daily variables."""
        return WeatherAPI.DAILY_VARIABLES.copy()
    
    @staticmethod
    def get_all_current_variables() -> List[str]:
        """Get all available current variables."""
        return WeatherAPI.CURRENT_VARIABLES.copy()
    
    @staticmethod
    def get_all_minutely_variables() -> List[str]:
        """Get all available 15-minutely variables."""
        return WeatherAPI.MINUTELY_15_VARIABLES.copy()
    
    @staticmethod
    def get_pressure_level_variables(level: int) -> List[str]:
        """
        Get all pressure level variables for a specific level.
        
        Args:
            level: Pressure level in hPa
            
        Returns:
            list: Pressure level variables for the specified level
        """
        if level not in WeatherAPI.PRESSURE_LEVELS:
            raise ValueError(f"Invalid pressure level: {level}")
            
        return [f"{var}_{level}hPa" for var in WeatherAPI.PRESSURE_LEVEL_VARIABLES]


# Create backward-compatible function wrappers
_api_client = WeatherAPI()

def get_forecast_data(location_data, days=7, forecast_types=None, custom_params=None):
    """
    Legacy function for getting forecast data.
    
    Args:
        location_data: Dictionary with lat, lng, and timezone
        days: Number of forecast days
        forecast_types: List of forecast types (e.g., ['hourly', 'daily'])
        custom_params: Custom parameters for each forecast type
        
    Returns:
        dict: Weather forecast data
    """
    # Convert string to list for backward compatibility
    if isinstance(forecast_types, str):
        forecast_types = [forecast_types]
    
    # Prepare parameters
    latitude = location_data['lat']
    longitude = location_data['lng']
    timezone = location_data.get('timezone', 'auto')
    
    # Build kwargs based on forecast types and custom params
    kwargs = {
        'timezone': timezone,
        'forecast_days': days
    }
    
    # Add parameters for each forecast type
    if forecast_types:
        for forecast_type in forecast_types:
            if forecast_type == 'hourly':
                params = custom_params.get('hourly', ["temperature_2m", "weather_code"]) if custom_params else ["temperature_2m", "weather_code"]
                kwargs['hourly'] = params
            elif forecast_type == 'daily':
                params = custom_params.get('daily', ["temperature_2m_max", "temperature_2m_min", "weather_code"]) if custom_params else ["temperature_2m_max", "temperature_2m_min", "weather_code"]
                kwargs['daily'] = params
            elif forecast_type == 'current':
                params = custom_params.get('current', ["temperature_2m", "weather_code"]) if custom_params else ["temperature_2m", "weather_code"]
                kwargs['current'] = params
    
    return _api_client.get_forecast(latitude, longitude, **kwargs)

def get_hourly_forecast(location_data, days=7):
    """Legacy function for getting hourly forecast."""
    return get_forecast_data(location_data, days, ['hourly'])

def get_daily_forecast(location_data, days=7):
    """Legacy function for getting daily forecast."""
    return get_forecast_data(location_data, days, ['daily'])

def get_current_weather(location_data):
    """Legacy function for getting current weather."""
    return get_forecast_data(location_data, 1, ['current'])

def get_complete_forecast(location_data, days=7):
    """Legacy function for getting complete forecast."""
    return get_forecast_data(location_data, days, ['hourly', 'daily', 'current'])