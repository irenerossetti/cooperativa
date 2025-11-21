from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import HarvestedProduct


@receiver(post_save, sender=HarvestedProduct)
def log_product_save(sender, instance, created, **kwargs):
    """Registrar creación/actualización de producto cosechado en auditoría"""
    from audit.utils import log_audit
    action = 'CREATE' if created else 'UPDATE'
    description = f'Producto {instance.product_name} - {instance.quantity}kg {"registrado" if created else "actualizado"}'
    
    log_audit(
        user=instance.created_by if created else None,
        action=action,
        model_name='HarvestedProduct',
        object_id=instance.id,
        description=description
    )


@receiver(post_delete, sender=HarvestedProduct)
def log_product_delete(sender, instance, **kwargs):
    """Registrar eliminación de producto cosechado en auditoría"""
    from audit.utils import log_audit
    log_audit(
        user=None,
        action='DELETE',
        model_name='HarvestedProduct',
        object_id=instance.id,
        description=f'Producto {instance.product_name} eliminado'
    )
