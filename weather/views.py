import requests
from django.conf import settings
from rest_framework.views import  APIView
from rest_framework.response import Response

class CurrentWeatherView(APIView):
    def get(self, request):
        city = request.query_params.get('city', 'kathmandu')
#city to lat/log
        geo_url = "https://api.openweathermap.org/geo/1.0/direct"
        geo_params = {
            'q' : city,
            'limit': 1,
            'appid' : settings.OPENWEATHER_API_KEY,
            
        }

        geo_response = requests.get(geo_url, params = geo_params)
        geo_data = geo_response.json()

        #error handling
        if not geo_data:
            return Response({"error": f"City '{city}' not found"}, status=404)
        
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        resolved_city = geo_data[0]['name']      # official name from geocoder
        country = geo_data[0]['country']

#conv lat/long to weather
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            'lat': lat,
            'lon': lon,
            'appid': settings.OPENWEATHER_API_KEY,
            'units': 'metric'
        }

        weather_response = requests.get(weather_url, params=weather_params)

        if weather_response.status_code != 200:
            return Response({"error": "Weather data unavailable"}, status=502)

        #convert to JSON
        data = weather_response.json()

        #clean response
        clean_data = {
            "city" : resolved_city,
            "country" : country,
            "lat" : lat,
            "lon" : lon,
            "temperature": data["main"]["temp"],
            "feels_like" : data["main"]["feels_like"],
            "temp_min" : data["main"]["temp_min"],
            "temp_max" : data["main"]["temp_max"],
            "humidity" : data.get("main", {}).get("humidity"),
            "condition" : data["weather"][0]["main"],
            
              
        }

        return Response(clean_data)
    

    
