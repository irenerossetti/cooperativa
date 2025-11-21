from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Shipment


@receiver(post_save, sender=Shipment)
def update_order_status_on_shipment(sender, instance, created, **kwargs):
    """Actualizar estado del pedido cuando cambia el estado del envío"""
    if instance.status == 'DELIVERED':
        order = instance.order
        order.status = 'DELIVERED'
        order.save()
    elif instance.status == 'IN_TRANSIT' and instance.order.status == 'PAID':
        order = instance.order
        order.status = 'SHIPPED'
        order.save()
