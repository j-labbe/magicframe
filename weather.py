import logging
import requests
from datetime import datetime
from requests.exceptions import RequestException
from os import getenv

class Weather:
    def __init__(self, latitude, longitude):
        self.logger = self.setup_logging()

        self.user_agent_domain = getenv('USER_AGENT_DOMAIN')
        self.user_agent_email = getenv('USER_AGENT_EMAIL')
        if not self.user_agent_domain or not self.user_agent_email:
            raise ValueError("User agent information is required from environment variables")

        if not latitude or not longitude:
            raise ValueError("Both latitude and longitude are required")

        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def setup_logging():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )
        # set logger name to module name
        logger = logging.getLogger("weather")
        return logger
    
    def get_weather(self):
        self.logger.info("Getting weather data")
        weather_data, error = self.get_forecast()
        if error:
            self.logger.error(f"Error getting weather data: {error}")
            return None, error

        cleaned_weather_data = self.get_forecast_from_weather(weather_data)

        self.logger.info("Weather data successfully retrieved")

        return cleaned_weather_data, None

    def make_request(self, url, headers):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), None
        except RequestException as e:
            self.logger.error(f"Request failed: {e}")
            return None, str(e)

    def get_forecast(self):
        self.logger.info("Getting forecast from National Weather Service API")

        headers = {
            "User-Agent": f"({self.user_agent_domain}, {self.user_agent_email})"
        }

        metadata_url = f'https://api.weather.gov/points/{self.latitude},{self.longitude}'
        metadata, error = self.make_request(metadata_url, headers)
        if error:
            return None, error

        forecast_url = metadata['properties']['forecast']
        station_url = metadata['properties']['observationStations']

        stations, error = self.make_request(station_url, headers)
        if error:
            return None, error

        if not stations['features']:
            self.logger.error("No observation stations found")
            return None, "No observation stations found"

        self.logger.info("Parsing observation stations")
        first_station_url = stations['features'][0]['id']

        current_temp, error = self.get_current_temperature(first_station_url)
        if error:
            return None, error

        forecast, error = self.make_request(forecast_url, headers)
        if error:
            return None, error

        return {"current_temperature": current_temp, "forecast": forecast}, None

    def get_current_temperature(self, station_url):
        self.logger.info(f"Getting current temperature from station: {station_url}")

        headers = {
            "User-Agent": f"({self.user_agent_domain}, {self.user_agent_email})"
        }

        observation, error = self.make_request(f"{station_url}/observations/latest", headers)
        if error:
            return None, error

        temperature_data = observation['properties']['temperature']
        if temperature_data['value'] is not None:
            if temperature_data['unitCode'] == 'unit:degF':
                temp_fahrenheit = temperature_data['value']
            else:
                temp_fahrenheit = (temperature_data['value'] * 9/5) + 32
            return temp_fahrenheit, None
        else:
            self.logger.error("Temperature data not available")
            return None, "Temperature data not available"

    def get_forecast_from_weather(self, weather_data):
        self.logger.info("Processing weather forecast data")

        def is_daytime(start_time_str, end_time_str):
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)
            day_start = start_time.replace(hour=6, minute=0, second=0, microsecond=0)
            day_end = start_time.replace(hour=18, minute=0, second=0, microsecond=0)
            return start_time >= day_start and end_time <= day_end

        filtered_forecast = []
        for day in weather_data["forecast"]["properties"]["periods"]:
            if is_daytime(day['startTime'], day['endTime']):
                filtered_forecast.append({
                    'day': day['name'],
                    'date': day['startTime'][:10],
                    'temperature': day['temperature'],
                    'conditions': self.summarize_condition(day['shortForecast'])
                })

        unique_forecast = []
        seen_dates = set()
        for forecast in filtered_forecast:
            if forecast['date'] not in seen_dates:
                unique_forecast.append(forecast)
                seen_dates.add(forecast['date'])

        return unique_forecast

    def summarize_condition(self, condition_text):

        condition_text = condition_text.lower()
        if any(cond in condition_text for cond in ['sunny', 'clear', 'fair', 'bright', 'sunshine']):
            return 'sunny'
        elif any(cond in condition_text for cond in ['cloudy', 'overcast', 'clouds', 'gloomy']):
            return 'cloudy'
        elif any(cond in condition_text for cond in ['rain', 'showers', 'drizzle', 'rainfall', 'wet', 'sprinkle']):
            return 'rainy'
        elif any(cond in condition_text for cond in ['snow', 'flurries', 'sleet', 'blizzard', 'snowfall', 'snowstorm']):
            return 'snowy'
        elif any(cond in condition_text for cond in ['storm', 'thunderstorm', 'severe', 'lightning', 'thunder', 'cyclone', 'hurricane', 'tornado']):
            return 'stormy'
        elif any(cond in condition_text for cond in ['fog', 'mist', 'haze', 'foggy', 'misty']):
            return 'foggy'
        elif any(cond in condition_text for cond in ['wind', 'breezy', 'gusty', 'windstorm']):
            return 'windy'
        elif any(cond in condition_text for cond in ['hot', 'heat', 'sweltering', 'scorching']):
            return 'hot'
        elif any(cond in condition_text for cond in ['cold', 'chill', 'chilly', 'freezing', 'frost']):
            return 'cold'
        else:
            return 'unknown'
