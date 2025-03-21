#Forecast class

class Forecast:

    def __init__(self, location, start_date, end_date, hourly_conditions, daily_conditions):
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.hourly_conditions = hourly_conditions
        self.daily_conditions = daily_conditions

    def _get_dominant_condition(self, hours):
        if not hours:
            return None
        
        code_counts = {}

        for hour in hours:
            code_counts[hour.weather_code] = code_counts.get(hour.weather_code, 0) + 1

        dominant_code = max(code_counts, key=code_counts.get)

        for hour in hours:
            if hour.weather_code == dominant_code:
                return hour

    def getDayForecast(self, date=None):
        if date is None:
            date = self.start_date

        daily_summary = None
        for day in self.daily_conditions:
            if day.time.date() == date.date():
                daily_summary = day
                break
        
        if not daily_summary:
            return None
        
        hours = []

        for hour in self.hourly_conditions:
            if hour.time.date() == date.date():
                hours.append(hour)

        precipitation_hours = sum(1 for h in hours if getattr(h, 'precipitation', 0) > 0.1)

        morning_hours = [h for h in hours if 6 <= h.time.hour < 12]
        afternoon_hours = [h for h in hours if 12 <= h.time.hour < 18]
        evening_hours = [h for h in hours if 18 <= h.time.hour < 22]

        morning_weather = self._get_dominant_condition(morning_hours) if morning_hours else None
        afternoon_weather = self._get_dominant_condition(afternoon_hours) if afternoon_hours else None
        evening_weather = self._get_dominant_condition(evening_hours) if evening_hours else None

        high_temp = max(hours, key=lambda h: h.temperature) if hours else None
        low_temp = min(hours, key=lambda h: h.temperature) if hours else None

        return {
                "date": date,
                "location": self.location,
                "summary": daily_summary,
                "high": {
                    "temp": high_temp.temperature if high_temp else daily_summary.high_temp,
                    "time": high_temp.time if high_temp else None
                },
                "low": {
                    "temp": low_temp.temperature if low_temp else daily_summary.low_temp,
                    "time": low_temp.time if low_temp else None
                },
                "precipitation_hours": precipitation_hours,
                "parts_of_day": {
                    "morning": morning_weather,
                    "afternoon": afternoon_weather, 
                    "evening": evening_weather
                },
                "hourly": hours,
                "emoji": daily_summary.getEmoji(),
                "description": daily_summary.getDescription()
            }

    def getHighLowTemps(self):
        pass

    def getSummary(self):
        pass