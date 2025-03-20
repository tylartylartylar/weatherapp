Here's the raw markdown text for the README:

# Weather App

A Python application for retrieving and displaying weather forecasts using the Open-Meteo API.

## Overview

This application allows users to check weather forecasts for any location in the United States using zipcode input. The app supports various forecast types including:

- Current weather conditions
- Daily forecasts
- Weekly (7-day) forecasts
- Extended (14-day) forecasts

## Project Structure

```
weatherapp/
├── forecasts/
│   ├── current.py     # Current weather display
│   ├── daily.py       # Daily forecast display
│   ├── extended.py    # 14-day forecast display
│   └── weekly.py      # 7-day forecast display
├── models/
│   ├── location.py    # Location data structures
│   └── weather.py     # Weather data structures
├── utils/
│   ├── config.py      # Configuration settings
│   ├── display.py     # Formatting and display utilities
│   ├── location.py    # Zipcode and location utilities
│   ├── weather_api.py # API interaction functions
│   └── zipcodes.csv   # Zipcode database
├── .gitignore
├── README.md
├── main.py            # Application entry point
└── requirements.txt   # Dependencies
```

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
2. Choose a forecast type (extended, weekly, or daily)

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
