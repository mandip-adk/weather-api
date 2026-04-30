from rest_framework.views import  APIView
from rest_framework.response import Response
from .services import get_weather, get_forecast
from .exceptions import CityNotFoundError, WeatherServiceError, GeocodingServiceError

class CurrentWeatherView(APIView):
    def get(self, request):
        city = request.query_params.get('city', 'kathmandu')

        try:
            weather = get_weather(city)
            return Response(weather)

        except CityNotFoundError as e:
            return Response({"error": str(e)}, status=404)

        except (WeatherServiceError, GeocodingServiceError) as e:
            return Response({"error": str(e)}, status=503)
    

class ForecastView(APIView):
    def get(self, request):
        city = request.query_params.get('city', 'kathmandu')
        days = request.query_params.get ('days', 5) 

         # query params come in as strings — convert to int
        try:
            days = int(days)
        except ValueError:
            return Response({"error": "days must be a number"}, status=400)

        if not 1 <= days <= 5:
            return Response({"error": "days must be between 1 and 5"}, status=400)

        try:
            forecast = get_forecast(city, days)
            return Response(forecast)

        except CityNotFoundError as e:
            return Response({"error": str(e)}, status=404)

        except (WeatherServiceError, GeocodingServiceError) as e:
            return Response({"error": str(e)}, status=503)
        
    
