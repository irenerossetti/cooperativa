from django.apps import AppConfig


class ShippingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shipping'
    verbose_name = 'Gestión de Envíos'

    def ready(self):
        import shipping.signals
