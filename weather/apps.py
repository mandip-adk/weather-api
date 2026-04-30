from django.apps import AppConfig
import os

class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'

    def ready(self):
        #runs once when django starts
        if os.environ.get ('RUN_MAIN') == 'true':

            from .task import start_background_task
            start_background_task()
        
