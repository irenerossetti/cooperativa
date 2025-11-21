from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import FarmActivity


@receiver(post_save, sender=FarmActivity)
def log_activity_save(sender, instance, created, **kwargs):
    """Registrar creación/actualización de labor en auditoría"""
    from audit.utils import log_audit
    action = 'CREATE' if created else 'UPDATE'
    description = f'Labor {instance.activity_type.get_name_display()} - {instance.parcel.code} {"registrada" if created else "actualizada"}'
    
    log_audit(
        user=instance.created_by if created else None,
        action=action,
        model_name='FarmActivity',
        object_id=instance.id,
        description=description
    )


@receiver(post_delete, sender=FarmActivity)
def log_activity_delete(sender, instance, **kwargs):
    """Registrar eliminación de labor en auditoría"""
    from audit.utils import log_audit
    log_audit(
        user=None,
        action='DELETE',
        model_name='FarmActivity',
        object_id=instance.id,
        description=f'Labor {instance.activity_type.get_name_display()} eliminada'
    )
