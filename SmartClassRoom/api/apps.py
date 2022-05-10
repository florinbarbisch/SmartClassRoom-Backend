from django.apps import AppConfig
from . import mqtt
import sys


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # See if django is testing
        TEST = 'test' in sys.argv
        if TEST:
            return
        # Start MQTT client
        print('API ready - Initializing MQTT')
        mqtt.client.loop_start()
