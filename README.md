# Weather App

A Python application for retrieving and displaying weather forecasts using the Open-Meteo API.

## Features

- Lookup location data by zipcode
- View different forecast types (current, daily, weekly, extended)
- Temperature conversion (Celsius to Fahrenheit)
- Weather condition descriptions
- Precipitation and wind data
- Subjective weather opinions

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/weatherapp.git
   cd weatherapp
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```
python main.py
```

Follow the prompts to:
1. Enter a zipcode
2. Displays debug and basic summary of today's weather.

## API Integration

This app uses the Open-Meteo API for weather data. The modular design in `weather_api.py` makes it easy to:

- Request different forecast types
- Customize parameters
- Handle API responses consistently

## Adding New Features

The application is designed to be modular and extensible:

1. **New Forecast Types**: Add a new file to the `forecasts/` directory
2. **New API Parameters**: Update the `FORECAST_PARAMS` dictionary in `weather_api.py`
3. **New Display Features**: Add functions to `display.py`

## Customization

Edit `utils/config.py` to modify:
- Weather code descriptions
- Days of the week labels
- Other application constants

## Credits

- Weather data provided by [Open-Meteo](https://open-meteo.com/)
- Zipcode database sourced from [Simple Maps](https://simplemaps.com/data/us-zips)
