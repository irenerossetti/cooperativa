from django.apps import AppConfig


class RequestsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'requests'
    verbose_name = 'Solicitudes de Socios'

    def ready(self):
        import requests.signals
