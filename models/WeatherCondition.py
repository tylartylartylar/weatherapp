# Weather data structures and models

class WeatherCondition:
    def __init__(self, time, temperature, weather_code, description, humidity, wind_speed, sunrise, sunset):
        self.time = time
        self.temperature = temperature
        self.weather_code = weather_code
        self.description = description
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.sunrise = sunrise
        self.sunset = sunset

    def getEmoji(self):
        if self.weather_code == 0:
            return "☀️"
        elif self.weather_code in [1,2,3]:
            return "🌤️"
        elif self.weather_code in [45, 48]:
            return "🌫️"
        elif self.weather_code in [51,53,55]:
            return "🌦️"
        elif self.weather_code in [61,63,65]:
            return "🌧️"
        elif self.weather_code in [56, 57, 66,67]:
            return "❄️☔"
        elif self.weather_code in [71,73,75, 77, 85, 86]:
            return "🌨️"
        elif self.weather_code == 95:
            return "🌩️"
        elif self.weather_code in [96,99]:
            return "🌩️🧊"
        else:
            return "🌤️ unknown condition"
        
    def getDescription(self):
        if self.weather_code == 0:
            return "clear sky"
        elif self.weather_code in [1,2,3]:
            return "partly cloudy"
        elif self.weather_code in [45, 48]:
            return "foggy"
        elif self.weather_code in [51,53,55]:
            return "drizzle"
        elif self.weather_code in [61,63,65]:
            return "rain"
        elif self.weather_code in [56, 57, 66, 67]:
            return "freezing rain"
        elif self.weather_code in [71,73,75, 77, 85, 86]:
            return "snow"
        elif self.weather_code == 95:
            return "thunderstorm"
        elif self.weather_code in [96,99]:
            return "thunderstorm with hail likely"
        else:
            return "unknown condition; probably certain death"
        
    def __str__(self):
        return self.getDescription()