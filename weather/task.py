import threading
import logging
from .services import get_weather

logger = logging.getLogger(__name__)

POPULAR_CITIES = ['Kathmandu', 'London', 'New York', 'Tokyo', 'Paris']


def fetch_popular_cities():
    logger.info("Background task started — fetching popular cities")

    for city in POPULAR_CITIES:
        try:
            weather = get_weather(city)
            logger.info(f"Fetched {city}: {weather['temperature']}°C")
        except Exception as e:
            logger.error(f"Failed to fetch {city}: {e}")

    logger.info("Background task complete")


def start_background_task():
    def run():
        fetch_popular_cities()
        timer = threading.Timer(1800, run)
        timer.daemon = True
        timer.start()

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
    logger.info("Background task thread started")

    