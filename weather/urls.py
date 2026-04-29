from django.urls import path
from weather.views import CurrentWeatherView

urlpatterns = [
    path('api/weather/', CurrentWeatherView.as_view()),
]
