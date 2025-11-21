from django.apps import AppConfig


class FarmActivitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'farm_activities'
    verbose_name = 'Labores Agrícolas'

    def ready(self):
        import farm_activities.signals
