from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PriceList


@receiver(post_save, sender=PriceList)
def log_price_list_save(sender, instance, created, **kwargs):
    """Registrar creación/actualización de lista de precios en auditoría"""
    from audit.utils import log_audit
    action = 'CREATE' if created else 'UPDATE'
    description = f'Lista de precios {instance.code} - {instance.name} {"creada" if created else "actualizada"}'
    
    log_audit(
        user=instance.created_by if created else None,
        action=action,
        model_name='PriceList',
        object_id=instance.id,
        description=description
    )
