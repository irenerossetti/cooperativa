from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Parcel


@receiver(post_save, sender=Parcel)
def log_parcel_save(sender, instance, created, **kwargs):
    """Registrar creación/actualización de parcela en auditoría"""
    from audit.utils import log_audit
    action = 'CREATE' if created else 'UPDATE'
    description = f'Parcela {instance.code} - {instance.name} {"creada" if created else "actualizada"}'
    
    log_audit(
        user=instance.created_by if created else None,
        action=action,
        model_name='Parcel',
        object_id=instance.id,
        description=description
    )


@receiver(post_delete, sender=Parcel)
def log_parcel_delete(sender, instance, **kwargs):
    """Registrar eliminación de parcela en auditoría"""
    from audit.utils import log_audit
    log_audit(
        user=None,
        action='DELETE',
        model_name='Parcel',
        object_id=instance.id,
        description=f'Parcela {instance.code} - {instance.name} eliminada'
    )
