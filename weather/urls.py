from django.urls import path
from weather.views import CurrentWeatherView, ForecastView

urlpatterns = [
    path('api/weather/', CurrentWeatherView.as_view()),
    path('api/forecast/', ForecastView.as_view()),
    
]
