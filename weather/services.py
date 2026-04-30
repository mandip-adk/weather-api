import requests
from django.conf import settings

def get_coordinates(city: str) -> dict:
##Convert city name to lat/lon using geocoding API
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        'q': city,
        'limit': 1,
        'appid': settings.OPENWEATHER_API_KEY
    }

    try:
        response = requests.get(url, params= params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestExceptoin:
        return None
    

    if not data:
        return {"error": "City not found"}
    
    return {
        'lat': data[0]['lat'],
        'lon': data[0]['lon'],
        'city': data[0]['name'],
        'country': data[0]['country'],
    }

def get_weather (city: str) -> dict:
#Main service function — takes city, returns clean weather data
    location = get_coordinates(city)

    if location is None:
        return {"error": "City not found"}
    
    url = "https://api.openweathermap.org/data/2.5/weather" #fetch weather using lat/lon
    params = {
        'lat': location['lat'],
        'lon': location['lon'],
        'appid': settings.OPENWEATHER_API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        return None


    return{
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

def get_forecast(city: str, days: int = 5) -> dict:

    location = get_coordinates(city)
    if location is None:
        return None
    
    # call forecast endpoint 
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'lat' : location['lat'],
        'lon' : location['lon'],
        'appid' : settings.OPENWEATHER_API_KEY,
        'units' : 'metric'
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
    
    data = response.json()

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
    
    return {
        'city': location['city'],
        'country': location['country'],
        'days': days,       # show user what they requested
        'total_entries': len(forecast_list), 
        'forecast': forecast_list        
    }

