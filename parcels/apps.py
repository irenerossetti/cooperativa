from django.apps import AppConfig


class ParcelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'parcels'
    verbose_name = 'Gestión de Parcelas'

    def ready(self):
        import parcels.signals
