from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Partner


@receiver(post_save, sender=Partner)
def log_partner_save(sender, instance, created, **kwargs):
    """Registrar creación/actualización de socio en auditoría"""
    from audit.utils import log_audit
    action = 'CREATE' if created else 'UPDATE'
    description = f'Socio {instance.full_name} (CI: {instance.ci}) {"creado" if created else "actualizado"}'
    
    log_audit(
        user=instance.created_by if created else None,
        action=action,
        model_name='Partner',
        object_id=instance.id,
        description=description
    )


@receiver(post_delete, sender=Partner)
def log_partner_delete(sender, instance, **kwargs):
    """Registrar eliminación de socio en auditoría"""
    from audit.utils import log_audit
    log_audit(
        user=None,
        action='DELETE',
        model_name='Partner',
        object_id=instance.id,
        description=f'Socio {instance.full_name} (CI: {instance.ci}) eliminado'
    )
