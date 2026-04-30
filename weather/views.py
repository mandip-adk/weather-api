from rest_framework.views import  APIView
from rest_framework.response import Response
from .services import get_weather, get_forecast

class CurrentWeatherView(APIView):
    def get(self, request):
        city = request.query_params.get('city', 'kathmandu')

        weather = get_weather(city)

        if weather is None:
            return Response ({"error": f"City '{city}' not found"}, status=404)
        
        return Response(weather)
    

class ForecastView(APIView):
    def get(self, request):
        city = request.query_params.get('city', 'kathmandu')
        days = request.query_params.get ('days', 5) 

         # query params come in as strings — convert to int
        try:
            days = int(days)
        except ValueError:
            return Response({"error": "days must be a number"}, status=400)

        # validate range
        if not 1 <= days <= 5:
            return Response({"error": "days must be between 1 and 5"}, status=400)
        
        forecast = get_forecast(city, days)

        if forecast is None:
            return Response({"error": f"City '{city}' not found"}, status=404)

        return Response(forecast)
    
