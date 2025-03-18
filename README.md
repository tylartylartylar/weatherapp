# Weather App

A simple console-based weather application that provides current weather conditions and hourly forecasts based on user location input.

## Features

- **Flexible Location Input**: Accept ZIP code, coordinates (latitude/longitude), or city/state
- **Current Weather Display**: Shows city name, current conditions, and high/low temperatures
- **Hourly Forecast**: Detailed hourly temperature breakdown throughout the day
- **Simple Console Interface**: Easy-to-use command-line application

## Requirements

- Python 3.7 or higher
- Internet connection for API access

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/weatherapp.git
   cd weatherapp
   ```

2. Set up a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Open-Meteo API key if required:
   ```
   OPEN_METEO_API_KEY=your_api_key_here
   ```
   Note: Open-Meteo offers free tier access which may not require an API key.

## Usage

Run the application:
```
python main.py
```

When prompted, enter your location in one of these formats:
- ZIP code: `12345`
- Coordinates: `40.7128,-74.0060`
- City, State: `New York, NY`

Example output:
```
Current Weather for New York, NY
Conditions: Partly Cloudy
High: 74°F | Low: 46°F

Hourly Forecast:
8AM: 52°F
9AM: 55°F
10AM: 59°F
11AM: 64°F
12PM: 68°F
1PM: 71°F
2PM: 73°F
3PM: 74°F
4PM: 72°F
5PM: 68°F
6PM: 63°F
7PM: 58°F
8PM: 54°F
```

## Technical Implementation

### API Integration
This project uses the Open-Meteo Weather API to fetch weather data. The application makes HTTP requests to the API endpoints based on the user's location input.

### Location Processing
The app includes logic to process and validate different types of location inputs:
- ZIP codes are validated for proper format
- Coordinates are checked for valid latitude/longitude ranges
- City/state inputs are formatted properly for API consumption

### Data Handling
The application retrieves and processes several types of weather data:
- Current conditions (temperature, weather description)
- Daily high and low temperatures
- Hourly temperature forecasts

## Project Structure

```
weatherapp/
├── main.py           # Main application entry point
├── src/
│   ├── api.py        # API integration logic
│   ├── location.py   # Location input processing
│   ├── weather.py    # Weather data processing
│   └── display.py    # Console display formatting
├── .env              # Environment variables (not in repo)
├── requirements.txt  # Project dependencies
└── README.md         # This file
```

## Future Enhancements

Potential features for future development:
- Weather preference index to rate how "perfect" the weather is based on user preferences
- Extended forecast for multiple days
- More detailed weather information (humidity, wind, etc.)
- Graphical visualizations of temperature changes
- Location history and favorite locations

## Acknowledgments

- [Open-Meteo](https://open-meteo.com/) for providing the weather data API
- All contributors to this project