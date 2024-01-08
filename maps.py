import requests
import os
import json
import math
import logging
from requests.exceptions import RequestException

class Maps:
    def __init__(self):
        self.logger = self.setup_logging()
        self.api_key = self._load_env_variable("MAPS_API_KEY")
        self.work_address = self._load_env_variable("WORK_ADDRESS")
        self.home_address = self._load_env_variable("HOME_ADDRESS")

    @staticmethod
    def setup_logging():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )
        # set logger name to module name
        logger = logging.getLogger("maps")
        return logger

    def _load_env_variable(self, name):
        value = os.getenv(name)
        if not value:
            logging.error(f"Environment variable {name} not found.")
            raise ValueError(f"Missing environment variable: {name}")
        return value

    def get_travel_time(self):
        self.logger.info("Getting travel time from Google Maps API")
        endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
        nav_request = f'origin={self.work_address}&destination={self.home_address}&departure_time=now&key={self.api_key}'
        request_url = endpoint + nav_request
        
        try:
            response = requests.get(request_url, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad requests (4XX or 5XX)
        except RequestException as e:
            logging.error(f"Error in the HTTP request: {e}")
            return "Error in the HTTP request"

        try:
            directions = response.json()
        except json.JSONDecodeError:
            logging.error("Error decoding the JSON response")
            return "Error decoding the JSON response"

        if directions.get("status") != "OK":
            logging.error(f"API error: {directions.get('status')}")
            return "Error from the API service"

        try:
            normal_duration = directions['routes'][0]['legs'][0]['duration']['value']  # In seconds
            traffic_duration = directions['routes'][0]['legs'][0]['duration_in_traffic']['value']  # In seconds
            traffic_delay = (traffic_duration - normal_duration) / 60  # Convert seconds to minutes
        except KeyError:
            logging.error("Error parsing the directions response")
            return "Error parsing the directions response"

        return math.ceil(traffic_duration / 60), math.ceil(traffic_delay)  # Convert seconds to minutes for total duration

# Example usage
# maps = Maps()
# travel_time, delay = maps.get_travel_time()
# print(f"Travel time: {travel_time} minutes, Delay: {delay} minutes")
