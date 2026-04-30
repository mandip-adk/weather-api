
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class WeatherAnonThrottle(AnonRateThrottle):
    rate = '5/minute' #anonymous user get 5/min for weather

class WeatherUserThrottle(UserRateThrottle):
    rate = '30/minute' #logged in users get 30/min for weather 

    