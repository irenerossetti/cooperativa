from django.apps import AppConfig


class AlertsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alerts'
    verbose_name = 'Sistema de Alertas'
    
    def ready(self):
        """Importar signals cuando la app esté lista"""
        import alerts.signals
