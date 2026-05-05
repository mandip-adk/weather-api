from django.urls import path
from weather.views import CurrentWeatherView, ForecastView, api_root
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
urlpatterns = [

    path('', api_root),

    #weather endpoints
    path('api/weather/', CurrentWeatherView.as_view()),
    path('api/forecast/', ForecastView.as_view()),
    
    #swagger
    path('api/schema/', SpectacularAPIView.as_view(), name= 'schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name = 'schema'), name = 'swagger-ui'),
    
]

