from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PartnerRequest


@receiver(post_save, sender=PartnerRequest)
def log_request_save(sender, instance, created, **kwargs):
    """Registrar creación/actualización de solicitud en auditoría"""
    from audit.utils import log_audit
    action = 'CREATE' if created else 'UPDATE'
    description = f'Solicitud {instance.request_number} - {instance.partner.full_name} {"creada" if created else "actualizada"}'
    
    log_audit(
        user=None,
        action=action,
        model_name='PartnerRequest',
        object_id=instance.id,
        description=description
    )
