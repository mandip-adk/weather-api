import requests
from django.conf import settings
from .exceptions import CityNotFoundError, WeatherServiceError, GeocodingServiceError

def get_coordinates(city: str) -> dict:
    # building params never fails — no try needed here
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        'q': city,
        'limit': 1,
        'appid': settings.OPENWEATHER_API_KEY
    }

    # try wraps ONLY the network call — this is where failures happen
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

    except requests.Timeout:
        raise GeocodingServiceError("Geocoding API timed out")

    except requests.RequestException:
        raise GeocodingServiceError("Geocoding API unreachable")

    if not data:
        raise CityNotFoundError(f"City '{city}' not found")

    return {
        'lat': data[0]['lat'],
        'lon': data[0]['lon'],
        'city': data[0]['name'],
        'country': data[0]['country'],
    }

def get_weather (city: str) -> dict:
    from django.core.cache import cache 
#Main service function — takes city, returns clean weather data
    
    #check cache first
    cache_key = f"weather_{city.lower().strip().replace(' ','_')}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    #cache miss- called external api
    location = get_coordinates(city)

    try:
    
        url = "https://api.openweathermap.org/data/2.5/weather" #fetch weather using lat/lon
        params = {
            'lat': location['lat'],
            'lon': location['lon'],
            'appid': settings.OPENWEATHER_API_KEY,
            'units': 'metric'
        }

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.Timeout:
        raise WeatherServiceError("Weather API timed out")

    except requests.RequestException:
        raise WeatherServiceError("Weather API unreachable")

    clean_data = {
        'city': location['city'],
        'country': location['country'],
        'lat': location['lat'],
        'lon': location['lon'],
        'temperature': data.get('main', {}).get('temp'),
        'feels_like': data.get('main', {}).get('feels_like'),
        'temp_min': data.get('main', {}).get('temp_min'),
        'temp_max': data.get('main', {}).get('temp_max'),
        'humidity': data.get('main', {}).get('humidity'),
        'condition': data.get('weather', [{}])[0].get('main'),
        

    }
    cache.set(cache_key, clean_data, timeout = 1800) #save to cache -30min

    return clean_data

def get_forecast(city: str, days: int = 5) -> dict:
    from django.core.cache import cache 
    cache_key = f"forecast_{city.lower().strip().replace(' ','_')}_{days}"
    cached = cache.get(cache_key)
    if cached:
        cached['from_cache'] = True
        return cached
    

    location = get_coordinates(city)
    
    try:
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            'lat': location['lat'],
            'lon': location['lon'],
            'appid': settings.OPENWEATHER_API_KEY,
            'units': 'metric'
        }

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

    except requests.Timeout:
        raise WeatherServiceError("Forecast API timed out")

    except requests.RequestException:
        raise WeatherServiceError("Forecast API unreachable")

    #calcu how many entries to return
    max_entries = days * 8

    forecast_list = []
    for entry in data['list'][: max_entries]:
        forecast_list.append({
            'datetime': entry['dt_txt'],
            'temperature': entry['main']['temp'],
            'feels_like': entry['main']['feels_like'],
            'humidity': entry['main']['humidity'],
            'condition': entry['weather'][0]['main'],
        })
    
    clean_data = {
        'city': location['city'],
        'country': location['country'],
        'days': days,       # show user what they requested
        'total_entries': len(forecast_list), 
        'forecast': forecast_list        
    }

    cache.set(cache_key, clean_data, timeout=1800)

    return clean_data

