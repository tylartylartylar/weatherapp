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