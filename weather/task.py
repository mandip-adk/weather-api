import threading
import logging
import time
from .services import get_weather, get_forecast

logger = logging.getLogger(__name__)

POPULAR_CITIES = ['Kathmandu', 'London', 'New York', 'Tokyo', 'Paris']


def fetch_popular_cities():
    logger.info("Background task started — warming cache")

    for city in POPULAR_CITIES:
        try:
            get_weather(city)
            get_forecast(city)
            logger.info(f"Cache warmed for {city}")
        except Exception as e:
            logger.error(f"Failed to warm cache for {city}: {e}")

    logger.info("Background task complete")


def start_background_task():
    def run():
        time.sleep(5)
        fetch_popular_cities()
        timer = threading.Timer(1800, run)
        timer.daemon = True
        timer.start()

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
    logger.info("Background task thread started")

    