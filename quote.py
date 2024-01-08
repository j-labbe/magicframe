import logging
import requests

class Quote:

    def __init__(self):
        self.logger = self.setup_logging()

    @staticmethod
    def setup_logging():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )
        # set logger name to module name
        logger = logging.getLogger("quote")
        return logger

    def get_quote(self):
        self.logger.info("Getting quote from ZenQuotes API")
        try:
            response = requests.get("https://zenquotes.io/api/today")
            response.raise_for_status()  # Raise an HTTPError for bad requests (4XX or 5XX)
            quote = response.json()[0]
            return quote['q'], quote['a']
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error in HTTP request: {e}")
            return "Error in HTTP request"