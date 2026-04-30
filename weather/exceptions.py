
class CityNotFoundError(Exception):
    """Geocoding returned no results for this city"""
    pass

class WeatherServiceError(Exception):
    """External weather API Failed"""
    pass

class GeocodingServiceError(Exception):
    """External geocoding API failed"""
    pass

