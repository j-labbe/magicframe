from datetime import datetime
from os import getenv
from maps import Maps
from quote import Quote
from weather import Weather

class ContentCreator:
    def __init__(self):
        
        self.latitude = getenv("WEATHER_LATITUDE")
        self.longitude = getenv("WEATHER_LONGITUDE")

        self.weather = Weather(self.latitude, self.longitude)
        self.maps = Maps()
        self.quote = Quote()

    def create_content(self):
        weather_data, error = self.weather.get_weather()
        if error:
            print(error)
            weather_data = {'current_temperature': 'N/A', 'forecast': 'N/A'}

        travel_time_with_traffic, traffic_delay = self.maps.get_travel_time()

        travel_metrics = {
            "time": travel_time_with_traffic,
            "delay": traffic_delay if traffic_delay > 0 else 0
        }

        quote = self.quote.get_quote()

        current_date = datetime.now()
        current_day = current_date.strftime("%d")
        current_month = current_date.strftime("%B")

        content = {
            "weather": weather_data,
            "travel": travel_metrics,
            "quote": quote,
            "date": {
                "current_day": current_day,
                "current_month": current_month
            }
        }

        return content
