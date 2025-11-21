from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Campaign


@receiver(post_save, sender=Campaign)
def log_campaign_save(sender, instance, created, **kwargs):
    """Registrar creación/actualización de campaña en auditoría"""
    from audit.utils import log_audit
    action = 'CREATE' if created else 'UPDATE'
    description = f'Campaña {instance.code} - {instance.name} {"creada" if created else "actualizada"}'
    
    log_audit(
        user=instance.created_by if created else None,
        action=action,
        model_name='Campaign',
        object_id=instance.id,
        description=description
    )


@receiver(post_delete, sender=Campaign)
def log_campaign_delete(sender, instance, **kwargs):
    """Registrar eliminación de campaña en auditoría"""
    from audit.utils import log_audit
    log_audit(
        user=None,
        action='DELETE',
        model_name='Campaign',
        object_id=instance.id,
        description=f'Campaña {instance.code} - {instance.name} eliminada'
    )
