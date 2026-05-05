from rest_framework.views import  APIView
from rest_framework.response import Response
from .services import get_weather, get_forecast
from .exceptions import CityNotFoundError, WeatherServiceError, GeocodingServiceError
from .throttles import WeatherAnonThrottle, WeatherUserThrottle
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import api_view


class CurrentWeatherView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [WeatherAnonThrottle, WeatherUserThrottle]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='city', type=str, description='City name', required=False),
        ],
        description= 'Get current weather for a city. Example: /api/weather/?city=London'        
    )

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
    permission_classes = [AllowAny]
    throttle_classes = [WeatherAnonThrottle, WeatherUserThrottle]

    @extend_schema(
            parameters=[
                OpenApiParameter(name='city', type=str, description='City name', required=False),
                OpenApiParameter(name = 'days', type=int, description='Number of days 1-5', required=False),
            ],
            description= 'Get weather forecast. Example: /api/forecast/?city=London&days=3'
    )
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



@api_view(['GET'])
def api_root(request):
    return Response({
        "message": "Welcome to Weather API",
        "usage": {
            "current_weather": "https://weather-api-ugdj.onrender.com/api/weather/?city=London",
            "forecast": "https://weather-api-ugdj.onrender.com/api/forecast/?city=London&days=3",
            "interactive_docs": "https://weather-api-ugdj.onrender.com/api/docs/"
        },
        "examples": {
            "kathmandu": "https://weather-api-ugdj.onrender.com/api/weather/?city=Kathmandu",
            "tokyo": "https://weather-api-ugdj.onrender.com/api/weather/?city=Tokyo",
            "london": "https://weather-api-ugdj.onrender.com/api/weather/?city=London",
        },
        "note": "Change the city parameter to any city in the world"
    })       
    
