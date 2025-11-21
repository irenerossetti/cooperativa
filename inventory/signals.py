from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InventoryItem, StockAlert


@receiver(post_save, sender=InventoryItem)
def check_stock_alert(sender, instance, **kwargs):
    """Crear alerta si el stock está bajo"""
    if instance.is_low_stock and not instance.alerts.filter(is_resolved=False).exists():
        StockAlert.objects.create(
            item=instance,
            current_stock=instance.current_stock,
            minimum_stock=instance.minimum_stock
        )
